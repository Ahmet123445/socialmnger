from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.platform_account import PlatformAccount
from app.models.system_setting import SystemSetting
from app.schemas.common import PlatformAccountCreate, PlatformAccountResponse, SystemSettingUpdate, SystemSettingResponse

router = APIRouter()


@router.get("/platforms", response_model=List[PlatformAccountResponse])
async def list_platform_accounts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(PlatformAccount).where(PlatformAccount.user_id == current_user.id)
    )
    return result.scalars().all()


@router.post("/platforms", response_model=PlatformAccountResponse)
async def add_platform_account(
    data: PlatformAccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = PlatformAccount(
        user_id=current_user.id,
        platform=data.platform,
        platform_username=data.platform_username,
        access_token=data.access_token,
        refresh_token=data.refresh_token,
        status="active" if data.access_token else "mock",
    )
    db.add(account)
    await db.flush()
    return account


@router.delete("/platforms/{account_id}")
async def remove_platform_account(
    account_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(PlatformAccount).where(PlatformAccount.id == account_id, PlatformAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Hesap bulunamadı")
    await db.delete(account)
    return {"message": "Hesap silindi"}


@router.get("/system", response_model=List[SystemSettingResponse])
async def list_system_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(SystemSetting))
    return result.scalars().all()


@router.put("/system", response_model=SystemSettingResponse)
async def update_system_setting(
    data: SystemSettingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(SystemSetting).where(SystemSetting.key == data.key))
    setting = result.scalar_one_or_none()

    if setting:
        setting.value = data.value
        if data.description:
            setting.description = data.description
    else:
        setting = SystemSetting(key=data.key, value=data.value, description=data.description)
        db.add(setting)

    await db.flush()
    return setting


@router.get("/health")
async def system_health():
    return {
        "status": "healthy",
        "services": {
            "backend": "running",
            "database": "connected",
            "redis": "connected",
            "storage": "available",
        },
        "publish_modes": {
            "youtube": "mock",
            "tiktok": "mock",
            "instagram": "mock",
            "twitter": "mock",
        },
    }
