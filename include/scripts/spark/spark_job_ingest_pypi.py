import time
import base64
import json
import sys
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
from typing import List, Union
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import SparkSession
from google.cloud import bigquery
from google.oauth2 import service_account

spark = SparkSession\
        .builder\
        .config("spark.sql.shuffle.partitions", "50")\
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")\
        .getOrCreate()

args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "ds",
        "date_end",
        "pypi_project",
        "target_table"
    ]
)

# Build local arguments
start_date = args["ds"]

if args["date_end"].lower() == "default":
    # If no end date is provided, default to the next day
    end_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
    end_date = end_date.strftime("%Y-%m-%d")
else:
    # Otherwise, use the provided end date
    end_date = args["date_end"]

pypi_project = args["pypi_project"]

if len(pypi_project.split(",")) > 1:
    # Handle multiple PyPI projects
    pypi_project = pypi_project.split(",")

target_table = args["target_table"]

def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f"Failed to fetch secret {secret_name} with exception {e}")
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

def pypi_file_downloads_query(
    pypi_project: Union[str, List[str]],
    start_date: str,
    end_date: str
) -> str:
    if isinstance(pypi_project, str):
        project_where_clause = f"project = '{pypi_project}'"
    elif isinstance(pypi_project, list):
        projects_str = ', '.join([f"'{p}'" for p in pypi_project])
        project_where_clause = f"project IN ({projects_str})"

    return f"""SELECT
    CAST(date_trunc(timestamp, DAY) AS DATE) AS download_date,
    project,
    file.version AS project_version,
    details.python AS python,
    details.system.name AS system_name,
    country_code,
    COUNT(project) AS download_count,
FROM `bigquery-public-data.pypi.file_downloads`
WHERE
    {project_where_clause}
    AND TIMESTAMP_TRUNC(timestamp, DAY) >= TIMESTAMP("{start_date}")
    AND TIMESTAMP_TRUNC(timestamp, DAY) < TIMESTAMP("{end_date}")
GROUP BY
    CAST(date_trunc(timestamp, DAY) AS DATE),
    project,
    file.version,
    country_code,
    details.python,
    details.system.name
"""

glueContext = GlueContext(spark.sparkContext)
spark = glueContext.spark_session

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS glue_catalog.mad_dashboard_dl.{target_table} (
        download_date DATE,
        project STRING,
        project_version STRING,
        python STRING,
        system_name STRING,
        country_code STRING,
        download_count INT
    )
    USING iceberg
    PARTITIONED BY(months(download_date))
""")

bigquery_query = pypi_file_downloads_query(
    pypi_project=pypi_project,
    start_date=start_date,
    end_date=end_date
)

# Retrieve BigQuery credentials
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name='us-west-2'
)

# BigQuery credentials
bigquery_credentials_secret = get_secret(secret_name = "BigQueryCredentials", region_name = "us-west-2")
bigquery_credentials_json = json.loads(base64.b64decode(json.loads(bigquery_credentials_secret)['credentials']))
bigquery_credentials = service_account.Credentials.from_service_account_info(bigquery_credentials_json)

# Instantiate BigQuery client
bigquery_client = bigquery.Client(project="mad-dashboard-app", credentials=bigquery_credentials)

# Fetch PyPI file downloads from BigQuery
print(f"Fetching PyPI file downloads from BigQuery with query:\n{bigquery_query}")
start_time = time.time()
pypi_project_table = bigquery_client.query(bigquery_query, timeout=300).to_arrow()
end_time = time.time()
print(f"{len(pypi_project_table)} records for PyPI file downloads fetched in {end_time - start_time} seconds.")

# Instantiate a PySpark DataFrame from the PyArrow Table
pypi_project_df = spark.createDataFrame(pypi_project_table.to_pandas())

# Insert Overwrite DataFrame to the target table
pypi_project_df\
    .write\
    .mode('overwrite')\
    .insertInto(f'glue_catalog.mad_dashboard_dl.{target_table}')

job = Job(glueContext)
