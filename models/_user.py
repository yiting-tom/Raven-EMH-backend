from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BANNED = "BANNED"
    DELETED = "DELETED"


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"


class UserDataInFirebaseAuth(BaseModel):
    localId: str
    email: EmailStr
    displayName: Optional[str]


class UserDataInFirestore(BaseModel):
    role: UserRole


class UserOutput(UserDataInFirestore, UserDataInFirebaseAuth):
    model_config = {
        "json_schema_extra": {
            "example": {
                "localId": "d882s72hfD8jfA7ejBpd9xjA73jD8",
                "email": "example@email",
                "displayName": "example name",
                "role": "PATIENT",
            }
        },
    }
