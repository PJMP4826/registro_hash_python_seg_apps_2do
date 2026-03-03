import jwt
from datetime import datetime, timezone
from src.domain.entities.token import TokenPayload
from src.infrastructure.config.settings import Settings
from src.domain.value_objects.auth_token import AuthToken
from src.domain.ports.jwt_service_port import TokenServicePort


class JWTService(TokenServicePort):
    def __init__(self, settings: Settings):
        self._jwt_secret_key = settings.jwt_secret_key
        self._jwt_refresh_secret_key = settings.jwt_refresh_secret_key
        self._algorithm = settings.jwt_algorithm

    def generate(self, payload: TokenPayload) -> AuthToken:
        access_token = self._encode(
            data={
                "sub": payload.subject,
                "claim": payload.claim,
                "exp": self._to_timestamp(dt=payload.expires_at),
                "iat": self._to_timestamp(dt=payload.iat),
            },
            secret=self._jwt_secret_key,
        )

        refresh_token = self._encode(
            data={
                "sub": payload.subject,
                "exp": self._to_timestamp(dt=payload.expires_at),
            },
            secret=self._jwt_refresh_secret_key,
        )

        return AuthToken(access_token=access_token, refresh_token=refresh_token)

    def validate(self, token: str) -> TokenPayload:
        try:
            data = jwt.decode(token, self._jwt_secret_key, algorithms=[self._algorithm])

            return TokenPayload(
                subject=data["sub"],
                expires_at=data["exp"],
                claim=data["claim"],
                iat=data["iat"],
            )

        except jwt.ExpiredSignatureError:
            raise Exception("Token expirado")
        except jwt.InvalidTokenError as e:
            raise Exception(f"Token invalido: {str(e)}")

        except Exception as e:
            raise e

    def _encode(self, data: dict, secret: str) -> str:
        return jwt.encode(payload=data, key=secret, algorithm=self._algorithm)

    def _to_timestamp(self, dt: datetime) -> int:
        return int(dt.astimezone(timezone.utc).timestamp())
