from typing import Annotated
from fastapi import Depends, status, HTTPException
from app.repository.user import UserRepository
from app.utils.init_repo import init_repo


class UserService:

    def __init__(
        self,
        user_repo: Annotated[
            UserRepository, Depends(init_repo(class_name=UserRepository))
        ],
    ):
        self.user_repo = user_repo

    def get_user(self, email: str):
        try:
            user = self.user_repo.get_user(email)
            if not user:
                return False
            return user

        except Exception as e:
            raise e


def init_user_service():
    return UserService(init_repo(class_name=UserRepository))
