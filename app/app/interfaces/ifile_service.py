from abc import ABC, abstractmethod
from typing import Optional
from app.schemas.file import FileBase


class IFileService(ABC):
    @abstractmethod
    def get_files(self, *, skip: int, limit: int) -> list[FileBase]:
        pass

    @abstractmethod
    async def get_file_by_id(self, film_id: str) -> Optional[FileBase]:
        pass

    @abstractmethod
    def get_file_by_name(self, *, name: str) -> FileBase:
        pass
