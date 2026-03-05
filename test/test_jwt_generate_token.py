from src.infrastructure.config.settings import settings
from src.infrastructure.security.jwt_service import JWTService
from datetime import datetime, timedelta, timezone


token_service = JWTService(settings=settings)

from src.domain.entities.token import TokenPayload

now = datetime.now(timezone.utc)

expiration_time = datetime.now() + timedelta(minutes=15)

payload = TokenPayload(
    subject="1651651",
    claim={"email": "test@gmail.com", "role": "admin"},
    expires_at=expiration_time,
    iat=datetime.now(),
)

token = token_service.generate(payload=payload)

print(f"token: {token.access_token}")
print(f"refresh token: {token.refresh_token}")
