from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class PlatformAccountCreate(BaseModel):
    platform: str
    platform_username: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class PlatformAccountResponse(BaseModel):
    id: UUID
    platform: str
    platform_username: Optional[str] = None
    platform_user_id: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class MediaAssetResponse(BaseModel):
    id: UUID
    filename: str
    original_filename: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    duration_seconds: Optional[int] = None
    thumbnail_path: Optional[str] = None
    storage_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class SystemSettingUpdate(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None


class SystemSettingResponse(BaseModel):
    id: UUID
    key: str
    value: Optional[str] = None
    description: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True


class PublishJobResponse(BaseModel):
    id: UUID
    content_item_id: UUID
    platform: str
    status: str
    attempts: int
    error_message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    today_content_count: int = 0
    week_content_count: int = 0
    scheduled_count: int = 0
    published_count: int = 0
    failed_count: int = 0
    total_views: int = 0
    total_likes: int = 0
    total_engagement_rate: float = 0.0
    platform_stats: dict = {}
    recent_content: list = []
    top_performing: Optional[dict] = None
    alerts: list = []
