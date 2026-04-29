import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    filename = Column(String(500), nullable=False)
    original_filename = Column(String(500), nullable=True)
    file_path = Column(String(1000), nullable=False)
    file_size = Column(BigInteger, nullable=True)
    mime_type = Column(String(100), nullable=True)
    duration_seconds = Column(BigInteger, nullable=True)
    thumbnail_path = Column(String(1000), nullable=True)
    storage_type = Column(String(50), default="local")  # local, minio
    created_at = Column(DateTime, default=datetime.utcnow)
