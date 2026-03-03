from src.infrastructure.config.settings import Settings

settings = Settings()

print(settings.jwt_secret_key)
print(settings.jwt_refresh_secret_key)
print(settings.jwt_algorithm)