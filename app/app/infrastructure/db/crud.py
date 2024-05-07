from app.models.db_file import FileDbModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid


async def db_create(db: AsyncSession, db_file: FileDbModel) -> FileDbModel:
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    return db_file


async def db_get_by_id(db: AsyncSession, file_id: uuid.UUID) -> FileDbModel:
    result = await db.execute(select(FileDbModel).filter(FileDbModel.id == file_id))
    return result.scalars().first()
