from typing import Dict, Type
from app.adapters.base import BasePlatformAdapter
from app.adapters.mock_adapter import MockAdapter
from app.adapters.youtube_adapter import YouTubeAdapter
from app.adapters.tiktok_adapter import TikTokAdapter
from app.adapters.instagram_adapter import InstagramAdapter
from app.adapters.twitter_adapter import TwitterAdapter

_adapters: Dict[str, BasePlatformAdapter] = {
    "youtube": YouTubeAdapter(),
    "tiktok": TikTokAdapter(),
    "instagram": InstagramAdapter(),
    "twitter": TwitterAdapter(),
}

_mock_adapter = MockAdapter()


def get_adapter(platform: str, mode: str = "mock") -> BasePlatformAdapter:
    if mode == "mock":
        return MockAdapter(platform)
    adapter = _adapters.get(platform)
    if not adapter:
        return MockAdapter(platform)
    return adapter


def get_all_adapters() -> Dict[str, BasePlatformAdapter]:
    return _adapters.copy()
