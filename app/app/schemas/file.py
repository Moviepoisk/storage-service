from uuid import UUID

from pydantic import BaseModel


class FileCreate(BaseModel):
    id: UUID
    path_in_storage: str
    filename: str
    size: int
    file_type: str
    short_name: str

class S3FileResult(BaseModel):
    path_in_storage: str
    filename: str
    size: int
    file_type: str
    short_name: str