from uuid import UUID
from datetime import datetime

from app.models.common import BaseOrjsonModel



class File(BaseOrjsonModel):
    id: UUID
    path_in_storage: str | None
    filename: str | None
    size: int
    file_type: str | None
    short_name: str | None
    created_at: datetime | None
