from pathlib import Path
from src.infrastructure.config.database import Database
from src.infrastructure.config.settings import Settings
from src.infrastructure.repository.user_repository import UserRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.security.jwt_service import JWTService

def get_settings() -> Settings:
    return Settings()

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / get_settings().database_name

def get_db_session() -> Database:
    db = Database()
    db.connect(str(DB_PATH))
    return db

def get_user_repository(db: Database):
    return UserRepository(db=db)

def get_password_hasher():
    return BcryptPasswordHasher()

def get_jwt_token_service() -> JWTService:
    return JWTService(settings=get_settings())