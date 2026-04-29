from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class PublishResult:
    success: bool
    platform: str
    platform_post_id: Optional[str] = None
    post_url: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AnalyticsResult:
    platform: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    follower_count: Optional[int] = None
    engagement_rate: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class BasePlatformAdapter(ABC):
    platform_name: str

    @abstractmethod
    async def validate_credentials(self, access_token: str) -> bool:
        pass

    @abstractmethod
    async def publish_video(
        self,
        access_token: str,
        video_path: str,
        caption: str,
        hashtags: str,
        **kwargs,
    ) -> PublishResult:
        pass

    @abstractmethod
    async def schedule_video(
        self,
        access_token: str,
        video_path: str,
        caption: str,
        hashtags: str,
        scheduled_at: datetime,
        **kwargs,
    ) -> PublishResult:
        pass

    @abstractmethod
    async def fetch_analytics(
        self,
        access_token: str,
        platform_post_id: str,
    ) -> AnalyticsResult:
        pass
