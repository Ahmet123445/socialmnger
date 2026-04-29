import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.db.base import Base


class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    media_asset_id = Column(UUID(as_uuid=True), ForeignKey("media_assets.id"), nullable=True)
    platforms = Column(ARRAY(String), nullable=True)  # ["youtube", "tiktok", "instagram", "twitter"]
    status = Column(String(50), default="draft")  # draft, scheduled, publishing, published, failed
    scheduled_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    general_caption = Column(Text, nullable=True)
    general_hashtags = Column(Text, nullable=True)
    platform_captions = Column(JSON, nullable=True)  # {"youtube": "...", "tiktok": "..."}
    platform_hashtags = Column(JSON, nullable=True)  # {"youtube": "...", "tiktok": "..."}
    ai_generated = Column(JSON, nullable=True)  # AI'nın ürettiği tüm varyasyonlar
    content_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
