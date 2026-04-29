import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content_item_id = Column(UUID(as_uuid=True), ForeignKey("content_items.id"), nullable=True)
    recommendation_type = Column(String(100), nullable=False)  # caption, hashtag, timing, content_style
    platform = Column(String(50), nullable=True)
    title = Column(String(500), nullable=True)
    recommendation = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=True)  # 0-1 arası
    context_data = Column(JSON, nullable=True)
    is_applied = Column(String(10), default="false")
    created_at = Column(DateTime, default=datetime.utcnow)
