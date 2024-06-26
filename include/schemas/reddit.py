from pydantic import BaseModel
from typing import List, Union, Optional, Tuple

class RedditSubmission(BaseModel):
    archived: bool
    author_fullname: Optional[Union[str, None]] = None
    author_flair_css_class: Union[str, None]
    author_flair_text: Union[str, None]
    category: Union[str, None]
    clicked: Union[bool, None]
    created: float
    created_utc: float
    distinguished: Union[str, None]
    domain: Union[str, None]
    downs: int
    edited: Union[bool, float]
    gilded: int
    gildings: Union[dict, None]
    hidden: Union[bool, None]
    hide_score: Union[bool, None]
    id: str
    is_created_from_ads_ui: Union[bool, None]
    is_meta: Union[bool, None]
    is_original_content: Union[bool, None]
    is_reddit_media_domain: Union[bool, None]
    is_self: bool
    is_video: bool
    link_flair_css_class: Union[str, None]
    link_flair_text: Union[str, None]
    locked: bool
    media: Union[dict, None]
    media_embed: Union[dict, None]
    media_only: bool
    name: str
    no_follow: Union[bool, None]
    num_comments: int
    num_crossposts: Union[int, None]
    over_18: Union[bool, None]
    parent_whitelist_status: Union[str, None]
    permalink: str
    pinned: bool
    pwls: int
    quarantine: bool
    removed_by_category: Union[str, None]
    saved: Union[bool, None]
    score: int
    secure_media: Union[dict, None]
    selftext: str
    selftext_html: Union[str, None]
    send_replies: Union[bool, None]
    spoiler: Union[bool, None]
    stickied: bool
    subreddit_id: str
    subreddit_name_prefixed: str
    subreddit_subscribers: int
    subreddit_type: Union[str, None]
    thumbnail: Union[str, None]
    title: str
    total_awards_received: Union[int, None]
    treatment_tags: Union[list, None]
    ups: int
    upvote_ratio: float
    url: str
    user_reports: Union[list, None]
    whitelist_status: Union[str, None]
    wls: Union[int, None]

class RedditComment(BaseModel):
    archived: bool
    author_fullname: Optional[Union[str, None]] = None
    author_flair_css_class: Union[str, None]
    author_flair_text: Union[str, None]
    awarders: Union[list, None]
    body: str
    body_html: Union[str, None]
    collapsed: Union[bool, None]
    collapsed_reason: Union[str, None]
    collapsed_reason_code: Union[str, None]
    controversiality: Union[int, None]
    created_utc: float
    distinguished: Union[str, None]
    downs: int
    edited: Union[bool, float]
    gilded: int
    gildings: Union[dict, None]
    id: str
    is_submitter: Union[bool, None]
    link_id: str
    locked: Union[bool, None]
    name: Union[str, None]
    no_follow: Union[bool, None]
    parent_id: str
    permalink: str
    score: int
    score_hidden: Union[bool, None]
    send_replies: Union[bool, None]
    stickied: bool
    subreddit_id: str
    subreddit_name_prefixed: str
    subreddit_type: Union[str, None]
    total_awards_received: Union[int, None]
    treatment_tags: Union[list, None]
    ups: int

reddit_submissions_schema = """
    archived BOOLEAN,
    author_fullname STRING,
    author_flair_css_class STRING,
    author_flair_text STRING,
    category STRING,
    clicked BOOLEAN,
    created DOUBLE,
    created_utc DOUBLE,
    distinguished STRING,
    domain STRING,
    downs INTEGER,
    edited DOUBLE,
    gilded INTEGER,
    gildings STRING,
    hidden BOOLEAN,
    hide_score BOOLEAN,
    id STRING,
    is_created_from_ads_ui BOOLEAN,
    is_meta BOOLEAN,
    is_original_content BOOLEAN,
    is_reddit_media_domain BOOLEAN,
    is_self BOOLEAN,
    is_video BOOLEAN,
    link_flair_css_class STRING,
    link_flair_text STRING,
    locked BOOLEAN,
    media STRING,
    media_embed STRING,
    media_only BOOLEAN,
    name STRING,
    no_follow BOOLEAN,
    num_comments INTEGER,
    num_crossposts INTEGER,
    over_18 BOOLEAN,
    parent_whitelist_status STRING,
    permalink STRING,
    pinned BOOLEAN,
    pwls INTEGER,
    quarantine BOOLEAN,
    removed_by_category STRING,
    saved BOOLEAN,
    score INTEGER,
    secure_media STRING,
    selftext STRING,
    selftext_html STRING,
    send_replies BOOLEAN,
    spoiler BOOLEAN,
    stickied BOOLEAN,
    subreddit_id STRING,
    subreddit_name_prefixed STRING,
    subreddit_subscribers INTEGER,
    subreddit_type STRING,
    thumbnail STRING,
    title STRING,
    total_awards_received INTEGER,
    treatment_tags STRING,
    ups INTEGER,
    upvote_ratio DOUBLE,
    url STRING,
    user_reports STRING,
    whitelist_status STRING,
    wls INTEGER,
    _fetched_date TEXT,
    _fetched_iso_utc TEXT
"""

reddit_comments_schema = """
    archived BOOLEAN,
    author_fullname STRING,
    author_flair_css_class STRING,
    author_flair_text STRING,
    awarders STRING,
    body STRING,
    body_html STRING,
    collapsed BOOLEAN,
    collapsed_reason STRING,
    collapsed_reason_code STRING,
    controversiality INTEGER,
    created_utc DOUBLE,
    distinguished STRING,
    downs INTEGER,
    edited DOUBLE,
    gilded INTEGER,
    gildings STRING,
    id STRING,
    is_submitter BOOLEAN,
    link_id STRING,
    locked BOOLEAN,
    name STRING,
    no_follow BOOLEAN,
    parent_id STRING,
    permalink STRING,
    score INTEGER,
    score_hidden BOOLEAN,
    send_replies BOOLEAN,
    stickied BOOLEAN,
    subreddit_id STRING,
    subreddit_name_prefixed STRING,
    subreddit_type STRING,
    total_awards_received INTEGER,
    treatment_tags STRING,
    ups INTEGER,
    _fetched_date TEXT,
    _fetched_iso_utc TEXT
"""