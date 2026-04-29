from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.ai_setting import AISetting
from app.models.ai_recommendation import AIRecommendation
from app.models.content_item import ContentItem
from app.schemas.ai import AISettingCreate, AISettingResponse, AIGenerateRequest, AIGenerateResponse, AIRecommendationResponse
from app.services.ai_service import AIService

router = APIRouter()


@router.get("/settings", response_model=List[AISettingResponse])
async def list_ai_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(AISetting).where(AISetting.user_id == current_user.id))
    return result.scalars().all()


@router.post("/settings", response_model=AISettingResponse)
async def create_or_update_ai_setting(
    data: AISettingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(AISetting).where(AISetting.user_id == current_user.id))
    existing = result.scalar_one_or_none()

    if existing:
        existing.provider = data.provider
        existing.base_url = data.base_url
        existing.api_key = data.api_key
        existing.model_name = data.model_name
        existing.temperature = data.temperature
        existing.max_tokens = data.max_tokens
        await db.flush()
        return existing

    setting = AISetting(
        user_id=current_user.id,
        provider=data.provider,
        base_url=data.base_url,
        api_key=data.api_key,
        model_name=data.model_name,
        temperature=data.temperature,
        max_tokens=data.max_tokens,
    )
    db.add(setting)
    await db.flush()
    return setting


@router.post("/generate", response_model=AIGenerateResponse)
async def generate_ai_content(
    data: AIGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(AISetting).where(AISetting.user_id == current_user.id))
    ai_setting = result.scalar_one_or_none()

    service = AIService(ai_setting)
    response = await service.generate_caption(
        platform=data.platform,
        title=data.title,
        description=data.description,
        existing_caption=data.existing_caption,
        generate_type=data.generate_type,
    )
    return response


@router.get("/recommendations", response_model=List[AIRecommendationResponse])
async def get_recommendations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(AIRecommendation)
        .where(AIRecommendation.user_id == current_user.id)
        .order_by(AIRecommendation.created_at.desc())
        .limit(20)
    )
    return result.scalars().all()


@router.post("/recommendations/generate")
async def generate_recommendations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(AISetting).where(AISetting.user_id == current_user.id))
    ai_setting = result.scalar_one_or_none()

    from app.models.analytics import AnalyticsSnapshot
    analytics_result = await db.execute(
        select(AnalyticsSnapshot).order_by(AnalyticsSnapshot.created_at.desc()).limit(50)
    )
    analytics_data = analytics_result.scalars().all()

    service = AIService(ai_setting)
    recommendations = await service.generate_recommendations(analytics_data)

    for rec in recommendations:
        recommendation = AIRecommendation(
            user_id=current_user.id,
            recommendation_type=rec.get("type", "general"),
            platform=rec.get("platform"),
            title=rec.get("title"),
            recommendation=rec.get("recommendation", ""),
            confidence_score=rec.get("confidence"),
            context_data=rec.get("context"),
        )
        db.add(recommendation)
    await db.flush()

    return {"message": f"{len(recommendations)} öneri üretildi", "count": len(recommendations)}
