import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.media_asset import MediaAsset
from app.schemas.common import MediaAssetResponse
from app.storage.minio_client import upload_file, get_file_url

router = APIRouter()

UPLOAD_DIR = "/tmp/sosyalmedya_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=MediaAssetResponse)
async def upload_media(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".mp4"
    unique_name = f"{uuid.uuid4()}{file_ext}"
    local_path = os.path.join(UPLOAD_DIR, unique_name)

    content = await file.read()
    with open(local_path, "wb") as f:
        f.write(content)

    try:
        file_path = upload_file(unique_name, local_path, file.content_type or "video/mp4")
        storage_type = "minio"
    except Exception:
        file_path = local_path
        storage_type = "local"

    asset = MediaAsset(
        user_id=current_user.id,
        filename=unique_name,
        original_filename=file.filename,
        file_path=file_path,
        file_size=len(content),
        mime_type=file.content_type or "video/mp4",
        storage_type=storage_type,
    )
    db.add(asset)
    await db.flush()
    return asset


@router.get("/", response_model=list[MediaAssetResponse])
async def list_media(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(MediaAsset).where(MediaAsset.user_id == current_user.id).order_by(MediaAsset.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{media_id}", response_model=MediaAssetResponse)
async def get_media(
    media_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(MediaAsset).where(MediaAsset.id == media_id, MediaAsset.user_id == current_user.id)
    )
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Medya bulunamadı")
    return asset


@router.get("/{media_id}/url")
async def get_media_url(
    media_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(MediaAsset).where(MediaAsset.id == media_id, MediaAsset.user_id == current_user.id)
    )
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Medya bulunamadı")

    try:
        url = get_file_url(asset.filename)
    except Exception:
        url = asset.file_path

    return {"url": url, "storage_type": asset.storage_type}
