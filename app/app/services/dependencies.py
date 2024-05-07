# from fastapi import Depends
from app.infrastructure.s3.minio import get_client_session
from app.infrastructure.s3.minio_service import MinioStorage
from miniopy_async import Minio
from app.core.config import settings


async def get_minio_storage() -> MinioStorage:
    minio_client = Minio(settings.minio_endpoint,
                         access_key=settings.minio_access_key,
                         secret_key=settings.minio_secret_key,
                         secure=False
                         )
    client_session = get_client_session()
    return MinioStorage(minio_client=minio_client, session_client=client_session)
