import os
from minio import Minio
from app.config import settings

_client = None


def get_minio_client() -> Minio:
    global _client
    if _client is None:
        _client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_SSL,
        )
        if not _client.bucket_exists(settings.MINIO_BUCKET):
            _client.make_bucket(settings.MINIO_BUCKET)
    return _client


def upload_file(object_name: str, file_path: str, content_type: str = "video/mp4") -> str:
    client = get_minio_client()
    client.fput_object(settings.MINIO_BUCKET, object_name, file_path, content_type=content_type)
    return f"minio://{settings.MINIO_BUCKET}/{object_name}"


def get_file_url(object_name: str, expires: int = 3600) -> str:
    client = get_minio_client()
    return client.presigned_get_object(settings.MINIO_BUCKET, object_name, expires=expires)


def delete_file(object_name: str) -> bool:
    try:
        client = get_minio_client()
        client.remove_object(settings.MINIO_BUCKET, object_name)
        return True
    except Exception:
        return False
