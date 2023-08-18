"""
models/_multimedia.py

This module defines the data models used in the FastAPI application for handling
multimedia files. These models are used for parsing and validating the data associated
with multimedia files uploaded by users.

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Classes:
    - MultimediaBase: The base model representing a multimedia file uploaded by a user.
    - MultimediaCreate: Model for validating the data when creating a new multimedia object.
    - MultimediaInDB: Model for representing a multimedia object stored in the database.
    - MultimediaInDBOutput: Model for representing the response data for a multimedia object.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MultimediaBase(BaseModel):
    """
    The base model representing a multimedia file uploaded by a user.

    Attributes:
        user_id (str): The ID of the user who uploaded the file.
        content_type (str): The content type of the file (e.g., "image/jpeg").
        file_data (bytes): The binary data of the uploaded file.
        filename (Optional[str]): The name of the uploaded file. Defaults to None.
        metadata (Optional[dict]): Additional metadata associated with the file. Defaults to an empty dict.
    """

    user_id: str
    content_type: str
    file_data: bytes
    filename: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)


class MultimediaCreate(MultimediaBase):
    """
    Model for validating the data when creating a new multimedia object.

    Inherits from MultimediaBase.
    """

    ...


class MultimediaInDB(MultimediaBase):
    """
    Model for representing a multimedia object stored in the database.

    Inherits from MultimediaBase.

    Attributes:
        id (str): The unique ID of the multimedia object in the database.
        created_at (datetime): The timestamp when the multimedia object was created. Defaults to the current UTC time.
    """

    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MultimediaInDBOutput(MultimediaBase):
    """
    Model for representing the response data for a multimedia object.

    Inherits from MultimediaBase.

    Attributes:
        id (str): The unique ID of the multimedia object.
        file_data (str): The binary data of the file, base64 encoded.
        created_at (datetime): The timestamp when the multimedia object was created. Defaults to the current UTC time.
    """

    id: str
    file_data: str
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
