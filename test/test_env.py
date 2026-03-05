from src.infrastructure.config.settings import settings


print(settings.jwt_secret_key)
print(settings.jwt_refresh_secret_key)
print(settings.jwt_algorithm)