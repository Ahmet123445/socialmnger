from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class AnalyticsResponse(BaseModel):
    id: UUID
    platform_post_id: UUID
    platform: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    follower_count: Optional[int] = None
    engagement_rate: Optional[float] = None
    performance_score: Optional[float] = None
    snapshot_date: datetime

    class Config:
        from_attributes = True


class AnalyticsSummary(BaseModel):
    total_views: int = 0
    total_likes: int = 0
    total_comments: int = 0
    total_shares: int = 0
    avg_engagement_rate: float = 0.0
    content_count: int = 0
    platform_breakdown: dict = {}


class DateRangeParams(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    platform: Optional[str] = None
