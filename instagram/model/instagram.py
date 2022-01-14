from dataclasses import dataclass
from datetime import datetime


@dataclass
class InstagramProfileDTO:
    userid: int
    username: str
    fullname: str
    biography: str
    external_url: str
    business_category_name: str
    is_business_account: bool
    is_private: bool
    profile_pic_url: str
    profile_pic_url_local: str
    total_followers: int
    total_followees: int
    media_count: int
    created_at: datetime
    updated_at: datetime


@dataclass
class InstagramProfileHistoryDTO:
    profile_spec: dict
    total_followers: int
    total_followees: int
    media_count: int
    updated_at: datetime


@dataclass
class InstagramPostDTO:
    username: str
    owner_username: str
    owner_id: str
    mediaid: str
    caption: str
    pcaption: str
    caption_hashtags: list
    caption_mentions: list
    title: str
    thumbnail_url: str
    thumbnail_url_local: str
    is_video: bool
    video_url: bool
    video_duration: float
    location_lat: float
    location_long: float
    post_date: datetime
    post_date_local: datetime
    post_date_utc: datetime
    created_at: datetime
    updated_at: datetime


@dataclass
class InstagramRelation:
    from_username: str
    to_username: str
    relation_type: str
    created_at: datetime = datetime.now()
