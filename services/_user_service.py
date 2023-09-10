from typing import List

from models import UserOutput
from repositories import UserRepo


class UserService:
    def __init__(self):
        self.repo = UserRepo()

    def get_all_users(self) -> List[UserOutput]:
        return self.repo.get_all_users()

    def get_user_by_id(self, user_id: str) -> UserOutput:
        return self.repo.get_user_by_id(user_id)
