from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.content_item import ContentItem
from app.models.platform_post import PlatformPost
from app.models.publish_job import PublishJob
from app.schemas.content import ContentItemCreate, ContentItemUpdate, ContentItemResponse, PlatformPostResponse, PublishRequest
from app.schemas.common import PublishJobResponse

router = APIRouter()


@router.get("/", response_model=List[ContentItemResponse])
async def list_content(
    status: Optional[str] = None,
    platform: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(ContentItem).where(ContentItem.user_id == current_user.id)
    if status:
        query = query.where(ContentItem.status == status)
    query = query.order_by(ContentItem.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{content_id}", response_model=ContentItemResponse)
async def get_content(
    content_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ContentItem).where(ContentItem.id == content_id, ContentItem.user_id == current_user.id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="İçerik bulunamadı")
    return item


@router.post("/", response_model=ContentItemResponse)
async def create_content(
    data: ContentItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = ContentItem(
        user_id=current_user.id,
        title=data.title,
        description=data.description,
        general_caption=data.general_caption,
        general_hashtags=data.general_hashtags,
        platforms=data.platforms,
        scheduled_at=data.scheduled_at,
        media_asset_id=data.media_asset_id,
        status="scheduled" if data.scheduled_at else "draft",
    )
    db.add(item)
    await db.flush()
    return item


@router.put("/{content_id}", response_model=ContentItemResponse)
async def update_content(
    content_id: UUID,
    data: ContentItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ContentItem).where(ContentItem.id == content_id, ContentItem.user_id == current_user.id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="İçerik bulunamadı")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    await db.flush()
    return item


@router.delete("/{content_id}")
async def delete_content(
    content_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ContentItem).where(ContentItem.id == content_id, ContentItem.user_id == current_user.id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="İçerik bulunamadı")
    await db.delete(item)
    return {"message": "İçerik silindi"}


@router.post("/publish", response_model=List[PublishJobResponse])
async def publish_content(
    data: PublishRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ContentItem).where(ContentItem.id == data.content_item_id, ContentItem.user_id == current_user.id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="İçerik bulunamadı")

    platforms = data.platforms or item.platforms or []
    if not platforms:
        raise HTTPException(status_code=400, detail="En az bir platform seçilmeli")

    jobs = []
    for platform in platforms:
        job = PublishJob(
            content_item_id=item.id,
            platform=platform,
            status="queued",
        )
        db.add(job)
        jobs.append(job)

    item.status = "publishing"
    await db.flush()

    from app.tasks.publish_tasks import publish_to_platform
    for job in jobs:
        task = publish_to_platform.delay(str(job.id))
        job.celery_task_id = task.id
    await db.flush()

    return jobs


@router.get("/{content_id}/posts", response_model=List[PlatformPostResponse])
async def get_content_posts(
    content_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(PlatformPost).where(PlatformPost.content_item_id == content_id)
    )
    return result.scalars().all()


@router.get("/{content_id}/jobs", response_model=List[PublishJobResponse])
async def get_content_jobs(
    content_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(PublishJob).where(PublishJob.content_item_id == content_id)
    )
    return result.scalars().all()
