from src.infrastructure.config.settings import settings
from src.infrastructure.security.jwt_service import JWTService


token_service = JWTService(settings=settings)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNjUxNjUxIiwiY2xhaW0iOnsiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsInJvbGUiOiJhZG1pbiJ9LCJleHAiOjE3NzI1NTQ5MTksImlhdCI6MTc3MjU1NDAxOX0.KP01S2LGDjV6v4IjJ87MnT26pM_SO3DkYLByhp3b1q4"
token_payload = token_service.validate(token)

print(f"token_payload: {token_payload}")
print(f"email: {token_payload.get_claim("email")}")
print(f"email: {token_payload.get_claim("role")}")
