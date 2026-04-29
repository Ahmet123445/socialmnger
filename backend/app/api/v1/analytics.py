from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional
from datetime import datetime, timedelta
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.analytics import AnalyticsSnapshot
from app.models.content_item import ContentItem
from app.models.platform_post import PlatformPost
from app.schemas.analytics import AnalyticsResponse, AnalyticsSummary

router = APIRouter()


@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    days: int = Query(30, ge=1, le=365),
    platform: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    start_date = datetime.utcnow() - timedelta(days=days)

    query = select(
        func.coalesce(func.sum(AnalyticsSnapshot.views), 0),
        func.coalesce(func.sum(AnalyticsSnapshot.likes), 0),
        func.coalesce(func.sum(AnalyticsSnapshot.comments), 0),
        func.coalesce(func.sum(AnalyticsSnapshot.shares), 0),
        func.coalesce(func.avg(AnalyticsSnapshot.engagement_rate), 0),
    ).where(AnalyticsSnapshot.created_at >= start_date)

    if platform:
        query = query.where(AnalyticsSnapshot.platform == platform)

    result = await db.execute(query)
    row = result.one()

    content_count_result = await db.execute(
        select(func.count(ContentItem.id)).where(
            and_(ContentItem.user_id == current_user.id, ContentItem.created_at >= start_date)
        )
    )
    content_count = content_count_result.scalar() or 0

    platform_query = select(
        AnalyticsSnapshot.platform,
        func.coalesce(func.sum(AnalyticsSnapshot.views), 0).label("views"),
        func.coalesce(func.sum(AnalyticsSnapshot.likes), 0).label("likes"),
    ).where(AnalyticsSnapshot.created_at >= start_date).group_by(AnalyticsSnapshot.platform)

    platform_result = await db.execute(platform_query)
    platform_breakdown = {}
    for pr in platform_result:
        platform_breakdown[pr.platform] = {"views": int(pr.views), "likes": int(pr.likes)}

    return AnalyticsSummary(
        total_views=int(row[0]),
        total_likes=int(row[1]),
        total_comments=int(row[2]),
        total_shares=int(row[3]),
        avg_engagement_rate=round(float(row[4]), 2),
        content_count=content_count,
        platform_breakdown=platform_breakdown,
    )


@router.get("/content/{content_id}", response_model=list[AnalyticsResponse])
async def get_content_analytics(
    content_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(AnalyticsSnapshot)
        .where(AnalyticsSnapshot.content_item_id == content_id)
        .order_by(AnalyticsSnapshot.snapshot_date.desc())
    )
    return result.scalars().all()


@router.get("/platform/{platform}", response_model=list[AnalyticsResponse])
async def get_platform_analytics(
    platform: str,
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    start_date = datetime.utcnow() - timedelta(days=days)
    result = await db.execute(
        select(AnalyticsSnapshot)
        .where(
            and_(AnalyticsSnapshot.platform == platform, AnalyticsSnapshot.created_at >= start_date)
        )
        .order_by(AnalyticsSnapshot.snapshot_date.desc())
    )
    return result.scalars().all()
