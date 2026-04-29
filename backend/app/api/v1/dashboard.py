from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.content_item import ContentItem
from app.models.platform_post import PlatformPost
from app.models.analytics import AnalyticsSnapshot
from app.models.publish_job import PublishJob
from app.schemas.common import DashboardSummary

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)

    today_result = await db.execute(
        select(func.count(ContentItem.id)).where(
            and_(ContentItem.user_id == current_user.id, ContentItem.created_at >= today_start)
        )
    )
    today_count = today_result.scalar() or 0

    week_result = await db.execute(
        select(func.count(ContentItem.id)).where(
            and_(ContentItem.user_id == current_user.id, ContentItem.created_at >= week_start)
        )
    )
    week_count = week_result.scalar() or 0

    scheduled_result = await db.execute(
        select(func.count(ContentItem.id)).where(
            and_(ContentItem.user_id == current_user.id, ContentItem.status == "scheduled")
        )
    )
    scheduled_count = scheduled_result.scalar() or 0

    published_result = await db.execute(
        select(func.count(ContentItem.id)).where(
            and_(ContentItem.user_id == current_user.id, ContentItem.status == "published")
        )
    )
    published_count = published_result.scalar() or 0

    failed_result = await db.execute(
        select(func.count(PublishJob.id)).where(PublishJob.status == "failed")
    )
    failed_count = failed_result.scalar() or 0

    analytics_result = await db.execute(
        select(
            func.coalesce(func.sum(AnalyticsSnapshot.views), 0),
            func.coalesce(func.sum(AnalyticsSnapshot.likes), 0),
            func.coalesce(func.avg(AnalyticsSnapshot.engagement_rate), 0),
        ).where(AnalyticsSnapshot.created_at >= week_start)
    )
    analytics_row = analytics_result.one()
    total_views = int(analytics_row[0])
    total_likes = int(analytics_row[1])
    avg_engagement = float(analytics_row[2]) if analytics_row[2] else 0.0

    recent_result = await db.execute(
        select(ContentItem)
        .where(ContentItem.user_id == current_user.id)
        .order_by(ContentItem.created_at.desc())
        .limit(5)
    )
    recent_items = recent_result.scalars().all()
    recent_content = [
        {
            "id": str(item.id),
            "title": item.title,
            "status": item.status,
            "platforms": item.platforms or [],
            "created_at": item.created_at.isoformat() if item.created_at else None,
        }
        for item in recent_items
    ]

    alerts = []
    if failed_count > 0:
        alerts.append({"type": "error", "message": f"{failed_count} başarısız yayınlama var"})
    if scheduled_count > 0:
        alerts.append({"type": "info", "message": f"{scheduled_count} içerik yayınlanmayı bekliyor"})

    return DashboardSummary(
        today_content_count=today_count,
        week_content_count=week_count,
        scheduled_count=scheduled_count,
        published_count=published_count,
        failed_count=failed_count,
        total_views=total_views,
        total_likes=total_likes,
        total_engagement_rate=round(avg_engagement, 2),
        recent_content=recent_content,
        alerts=alerts,
    )
