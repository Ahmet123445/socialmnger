import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform_post_id = Column(UUID(as_uuid=True), ForeignKey("platform_posts.id"), nullable=False)
    content_item_id = Column(UUID(as_uuid=True), ForeignKey("content_items.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    views = Column(BigInteger, default=0)
    likes = Column(BigInteger, default=0)
    comments = Column(BigInteger, default=0)
    shares = Column(BigInteger, default=0)
    saves = Column(BigInteger, default=0)
    follower_count = Column(BigInteger, nullable=True)
    engagement_rate = Column(Float, nullable=True)
    performance_score = Column(Float, nullable=True)  # 0-100 arası
    analytics_metadata = Column(JSON, nullable=True)
    snapshot_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
