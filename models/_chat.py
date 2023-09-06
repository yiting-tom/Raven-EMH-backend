from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Status(str, Enum):
    ACTIVATING = "ACTIVATING"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"


class ChatBase(BaseModel):
    user_id: str
    request: str
    parent_id: str


class ChatCreateInput(ChatBase):
    ...


class ChatCreate(ChatBase):
    response: str
    audio_id: str
    video_id: str
    status: Status
    children_ids: List[str]

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "user_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "request": "Hello, world!",
                "response": "Hello, world!",
                "parent_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "audio_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "video_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "status": "ACTIVATING",
            },
        }


class ChatInDB(ChatBase):
    id: str
    response: str
    audio_id: str
    video_id: str
    status: Status
    children_ids: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ChatUpdate(BaseModel):
    user_id: Optional[str] = None
    request: Optional[str] = None
    response: Optional[str] = None
    audio_id: Optional[str] = None
    video_id: Optional[str] = None
    status: Optional[Status] = None
    parent_id: Optional[str] = None
    children_ids: Optional[List[str]] = None


class ChatInDBOutput(ChatBase):
    id: str
    response: str
    status: Status
    parent_id: str
    children_ids: List[str]
    audio: Optional[str]
    video: Optional[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "user_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "request": "Hello, world!",
                "response": "Hello, world!",
                "status": "ACTIVATING",
                "parent_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "children_ids": ["5f9d9a9d9a9d9a9d9a9d9a9d"],
                "audio": b"UklGRkZ6BwBXQVZFZm10IBAAAAABAAEAwF0AAIC7AAAC...",
                "video": b"UklGRkZ6BwBXQVZFZm10IBAAAAABAAEAwF0AAIC7AAAC...",
            },
        },
    }
