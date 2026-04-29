from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime


class ContentItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    general_caption: Optional[str] = None
    general_hashtags: Optional[str] = None
    platforms: List[str] = []
    scheduled_at: Optional[datetime] = None
    media_asset_id: Optional[UUID] = None


class ContentItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    general_caption: Optional[str] = None
    general_hashtags: Optional[str] = None
    platforms: Optional[List[str]] = None
    platform_captions: Optional[Dict[str, str]] = None
    platform_hashtags: Optional[Dict[str, str]] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None
    media_asset_id: Optional[UUID] = None


class ContentItemResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    media_asset_id: Optional[UUID] = None
    platforms: Optional[List[str]] = None
    status: str
    scheduled_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    general_caption: Optional[str] = None
    general_hashtags: Optional[str] = None
    platform_captions: Optional[Dict[str, str]] = None
    platform_hashtags: Optional[Dict[str, str]] = None
    ai_generated: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlatformPostResponse(BaseModel):
    id: UUID
    content_item_id: UUID
    platform: str
    platform_post_id: Optional[str] = None
    caption: Optional[str] = None
    hashtags: Optional[str] = None
    status: str
    error_message: Optional[str] = None
    post_url: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PublishRequest(BaseModel):
    content_item_id: UUID
    platforms: Optional[List[str]] = None  # None = tüm seçili platformlar
