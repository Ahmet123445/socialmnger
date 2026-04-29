from app.adapters.base import BasePlatformAdapter, PublishResult, AnalyticsResult
from datetime import datetime
import random
import uuid


class MockAdapter(BasePlatformAdapter):
    def __init__(self, platform_name: str = "mock"):
        self.platform_name = platform_name

    async def validate_credentials(self, access_token: str) -> bool:
        return True

    async def publish_video(
        self,
        access_token: str,
        video_path: str,
        caption: str,
        hashtags: str,
        **kwargs,
    ) -> PublishResult:
        mock_post_id = f"mock_{uuid.uuid4().hex[:12]}"
        return PublishResult(
            success=True,
            platform=self.platform_name,
            platform_post_id=mock_post_id,
            post_url=f"https://mock.{self.platform_name}.com/watch/{mock_post_id}",
            metadata={
                "mock": True,
                "published_at": datetime.utcnow().isoformat(),
                "message": f"[MOCK] {self.platform_name} platformuna başarıyla yayınlandı",
            },
        )

    async def schedule_video(
        self,
        access_token: str,
        video_path: str,
        caption: str,
        hashtags: str,
        scheduled_at: datetime,
        **kwargs,
    ) -> PublishResult:
        mock_post_id = f"scheduled_{uuid.uuid4().hex[:12]}"
        return PublishResult(
            success=True,
            platform=self.platform_name,
            platform_post_id=mock_post_id,
            metadata={
                "mock": True,
                "scheduled_at": scheduled_at.isoformat(),
                "message": f"[MOCK] {self.platform_name} platformunda zamanlandı",
            },
        )

    async def fetch_analytics(
        self,
        access_token: str,
        platform_post_id: str,
    ) -> AnalyticsResult:
        return AnalyticsResult(
            platform=self.platform_name,
            views=random.randint(100, 50000),
            likes=random.randint(10, 5000),
            comments=random.randint(0, 500),
            shares=random.randint(0, 1000),
            saves=random.randint(0, 200),
            follower_count=random.randint(100, 100000),
            engagement_rate=round(random.uniform(1.0, 15.0), 2),
            metadata={"mock": True},
        )
