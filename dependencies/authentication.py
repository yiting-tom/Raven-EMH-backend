from functools import wraps
from typing import List

from fastapi import HTTPException, Request
from firebase_admin import auth

from models import UserOutput, UserRole
from services import UserService

user_service = UserService()


def get_user_id(request: Request):
    id_token = request.headers.get("Authorization", "").split("Bearer ")[-1]

    if not id_token:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid: str = decoded_token["uid"]
        return uid
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")


def requires_roles(roles: List[UserRole]):
    def decorator(func):
        @wraps(func)
        async def decorated_func(request: Request, *args, **kwargs):
            user_id: str = get_user_id(request)
            user: UserOutput = user_service.get_user_by_id(user_id)
            if user.role not in roles:
                raise HTTPException(status_code=403, detail="Not enough permissions")

            return await func(request, *args, **kwargs)

        return decorated_func

    return decorator
