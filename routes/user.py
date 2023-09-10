from typing import List
from fastapi import APIRouter, Depends, HTTPException

from models import UserOutput
from services import UserService

router = APIRouter()

service = UserService()


@router.get("/", response_model=List[UserOutput])
def get_all_users():
    return service.get_all_users()
