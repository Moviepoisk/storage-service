from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()


class FileDbModel(Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path_in_storage = Column(String(255), nullable=False, unique=True)
    filename = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    file_type = Column(String(100), nullable=True)
    short_name = Column(String(24), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, path_in_storage: str, filename: str, short_name: str,
                 size: int, file_type: str, id: Optional[uuid.UUID] = None):
        self.id = id if id else uuid.uuid4()
        self.path_in_storage = path_in_storage
        self.filename = filename
        self.short_name = short_name
        self.size = size
        self.file_type = file_type

    def __repr__(self):
        return f'<File {self.filename}>'


# Создание индексов
Index('idx_file_path', FileDbModel.path_in_storage)
Index('idx_file_short_name', FileDbModel.short_name)
