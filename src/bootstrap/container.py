from src.application.use_cases.create_user import CreateUser
from .providers import (
    get_db_session,
    get_user_repository,
    get_password_hasher,
    get_jwt_token_service
)
from src.application.use_cases.change_password import ChangePassword
from src.application.use_cases.change_rol import ChangeUserRol
from src.application.use_cases.authenticate_user import AuthenticateUser
from src.application.use_cases.validate_token import ValidateTokenUseCase
from presentation.middleware.auth_middleware import JWTMiddleware


class Container:
    def __init__(self):
        self.db = get_db_session()
        self.user_repo = get_user_repository(self.db)
        self.hasher = get_password_hasher()
        self.jwt_service = get_jwt_token_service()

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
    
    def change_rol_use_case(self) -> ChangeUserRol:
        return ChangeUserRol(
            repo=self.user_repo,
            hasher=self.hasher
        )
    
    def login_use_case(self) -> AuthenticateUser:
        return AuthenticateUser(
            repo=self.user_repo,
            hasher=self.hasher,
            token_service=self.jwt_service
        )
    
    def validate_token_use_case(self) -> ValidateTokenUseCase:
        return ValidateTokenUseCase(
            token_service=self.jwt_service
        )
    
    def get_json_middleware(self) -> JWTMiddleware:
        return JWTMiddleware(validate_token_use_case=self.validate_token_use_case())
