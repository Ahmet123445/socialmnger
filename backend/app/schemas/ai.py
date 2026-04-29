from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class AISettingCreate(BaseModel):
    provider: str = "openai"
    base_url: str = "https://api.openai.com/v1"
    api_key: Optional[str] = None
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000


class AISettingResponse(BaseModel):
    id: UUID
    provider: str
    base_url: str
    model_name: str
    temperature: float
    max_tokens: int
    is_active: str
    created_at: datetime

    class Config:
        from_attributes = True


class AIGenerateRequest(BaseModel):
    content_item_id: Optional[UUID] = None
    platform: str  # youtube, tiktok, instagram, twitter
    title: str
    description: Optional[str] = None
    existing_caption: Optional[str] = None
    generate_type: str = "caption"  # caption, hashtags, all


class AIGenerateResponse(BaseModel):
    platform: str
    caption: Optional[str] = None
    hashtags: Optional[str] = None
    suggestions: Optional[list] = None


class AIRecommendationResponse(BaseModel):
    id: UUID
    recommendation_type: str
    platform: Optional[str] = None
    title: Optional[str] = None
    recommendation: str
    confidence_score: Optional[float] = None
    is_applied: str
    created_at: datetime

    class Config:
        from_attributes = True
