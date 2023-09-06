from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Annotation(BaseModel):
    created_at: datetime
    created_by: str  # the doctor's id
    score: int  # 1-5


class FeedbackBase(BaseModel):
    user_id: str
    username: str
    request: str
    response: str
    parent_id: str
    annotations: List[Annotation] = Field(default_factory=list)


class FeedbackCreateInput(FeedbackBase):
    ...


class FeedbackCreate(FeedbackBase):
    ...

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "user_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "username": "Test User",
                "request": "Hello, world!",
                "response": "Hello, world!",
                "parent_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "annotation": [
                    {
                        "created_at": "2023-10-10 10:10",
                        "created_by": "test_doctor",
                        "score": 5,
                    },
                    {
                        "created_at": "2023-10-10 12:10",
                        "created_by": "test_doctor_2",
                        "score": 4,
                    },
                ],
            },
        }


class FeedbackInDB(FeedbackCreate):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class FeedbackUpdate(BaseModel):
    annotations: List[Annotation] = Field(default_factory=list)


class FeedbackInDBOutput(FeedbackInDB):
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "username": "Test User",
                "request": "Hello, world!",
                "response": "Hello, world!",
                "parent_id": "5f9d9a9d9a9d9a9d9a9d9a9d",
                "create_at": "2023-10-10 10:10",
                "updated_at": "2023-10-10 10:10",
                "annotation": [
                    {
                        "created_at": "2023-10-10 10:10",
                        "created_by": "test_doctor",
                        "score": 5,
                    },
                    {
                        "created_at": "2023-10-10 12:10",
                        "created_by": "test_doctor_2",
                        "score": 4,
                    },
                ],
            },
        },
    }
