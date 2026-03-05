from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )  # type: ignore

    # Database Configuration
    database_name: str = Field(..., description="Name of the SQLite Database")

    # JWT Configuracion
    jwt_secret_key: str = Field(..., description="JWT Secret Key")
    jwt_refresh_secret_key: str = Field(..., description="JWT Refresh Secret Key")
    jwt_algorithm: str = Field(..., description="JWT algorithm")
    jwt_expires_in_minutes: int = Field(..., description="Token expiration in minutes")



settings = Settings()  # type: ignore
