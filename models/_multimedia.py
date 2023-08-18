from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel


class MultimediaBase(BaseModel):
    user_id: str
    content_type: str
    file_data: bytes
    filename: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)


class MultimediaCreate(MultimediaBase):
    ...


class MultimediaInDB(MultimediaBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MultimediaInDBOutput(MultimediaBase):
    id: str
    file_data: str              # base64 encoded
    created_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "5f3c4e8c2e4a4c8e7a5e7d2e",
                "user_id": "5f3c4e8c2e4a4c8e7a5e7d2e",
                "content_type": "image/jpeg",
                "file_data": "UklGRkZ6BwBXQVZFZm10IBAAAAABAAEAwF0AAIC7AAAC...",
                "filename": "image.jpeg",
                "metadata": {},
                "created_at": "2020-08-19T00:00:00",
            },
        }

