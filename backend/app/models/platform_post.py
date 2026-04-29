import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class PlatformPost(Base):
    __tablename__ = "platform_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_item_id = Column(UUID(as_uuid=True), ForeignKey("content_items.id"), nullable=False)
    platform_account_id = Column(UUID(as_uuid=True), ForeignKey("platform_accounts.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    platform_post_id = Column(String(255), nullable=True)  # Platform'daki post ID'si
    caption = Column(Text, nullable=True)
    hashtags = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending, publishing, published, failed
    error_message = Column(Text, nullable=True)
    post_url = Column(String(1000), nullable=True)
    published_at = Column(DateTime, nullable=True)
    platform_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
