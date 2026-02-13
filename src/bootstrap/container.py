from src.application.use_cases.create_user import CreateUser
from .providers import (
    get_db_session,
    get_user_repository,
    get_password_hasher
)
from ..application.use_cases.change_password import ChangePassword


class Container:
    def __init__(self):
        self.db = get_db_session()
        self.user_repo = get_user_repository(self.db)
        self.hasher = get_password_hasher()

    def create_user_use_case(self) -> CreateUser:
        return CreateUser(
            repo=self.user_repo,
            hasher=self.hasher
        )

    def change_password_use_case(self) -> ChangePassword:
        return ChangePassword (
            repo=self.user_repo,
            hasher=self.hasher
        )