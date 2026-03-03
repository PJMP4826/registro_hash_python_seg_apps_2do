from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.domain.entities.user import User
from src.domain.ports.jwt_service_port import TokenServicePort
from src.application.use_cases.validate_token import ValidateTokenUseCase


class JWTMiddleware:
    def __init__(self, validate_token_use_case: ValidateTokenUseCase):
        self._validate_token = validate_token_use_case
        self._bearer_scheme = HTTPBearer()

    def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ) -> User:
        return self._authenticate(credentials.credentials)

    def require_role(self, role: str):
        def dependency(
            credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        ) -> dict[str, str]:
            user = self._authenticate(credentials.credentials)
            if user["role"] != role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Se requiere el rol: {role}",
                )
            return user
        return dependency

    def _authenticate(self, token: str) -> dict[str, str]:
        try:
            payload = self._validate_token.execute(token)
            
            return {
                "uuid": payload.subject,
                "email": payload.get_claim("email"),
                "role": payload.get_claim("role")
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )