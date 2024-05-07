from http import HTTPStatus
from uuid import UUID
from fastapi import APIRouter, Depends, File, HTTPException
from fastapi.datastructures import UploadFile
from app.services.dependencies import get_minio_storage
from app.infrastructure.s3.minio_service import MinioStorage

from app.infrastructure.db.database import get_session
from app.infrastructure.db.crud import db_create, db_get_by_id

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse


from app.models.db_file import FileDbModel
from uuid import uuid4


router = APIRouter()


@router.post("/")
async def create_file(file: UploadFile = File(...),
                      db: AsyncSession = Depends(get_session),
                      storage: MinioStorage = Depends(get_minio_storage)
                      ):

    s3_result = await storage.save(file)

    if s3_result is not None:
        unique_id = str(uuid4())
        file_db_model_with_id = FileDbModel(
            id=unique_id,  
            path_in_storage=s3_result.path_in_storage,
            filename=s3_result.filename,
            short_name=s3_result.short_name,
            size=s3_result.size,
            file_type=s3_result.file_type
        )
        await db_create(db, file_db_model_with_id)
        return unique_id
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Не удалось, проблема с S3")


@router.get("/{file_id}")
async def get_streaming_file(
        file_id: UUID, db_session: AsyncSession = Depends(get_session),
        storage: MinioStorage = Depends(get_minio_storage)):
    file_meta = await db_get_by_id(db_session, file_id)
    if not file_meta:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Meta not found")

    filename = file_meta.path_in_storage.split("/")[-1]
    file_streamer = await storage.get_file_stream('movies', filename)
    if file_streamer is None:
        # Обработка ошибки, если файл не найден или другая ошибка S3
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="File not found")
    return StreamingResponse(file_streamer(), media_type="application/octet-stream")
