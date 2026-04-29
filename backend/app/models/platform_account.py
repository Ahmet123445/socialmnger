import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class PlatformAccount(Base):
    __tablename__ = "platform_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # youtube, tiktok, instagram, twitter
    platform_user_id = Column(String(255), nullable=True)
    platform_username = Column(String(255), nullable=True)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    platform_metadata = Column(JSON, nullable=True)
    status = Column(String(50), default="active")  # active, expired, error, disconnected
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
