from pathlib import Path
from src.infrastructure.config.database import Database
from src.infrastructure.config.settings import settings
from src.infrastructure.repository.user_repository import UserRepository
from src.infrastructure.repository.departamento_repository import DepartamentoRepository
from src.infrastructure.repository.inquilino_repository import InquilinoRepository
from src.infrastructure.repository.cuota_repository import CuotaRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.security.jwt_service import JWTService


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / settings.database_name


def get_db_session() -> Database:
    db = Database()
    db.connect(str(DB_PATH))
    return db


def get_user_repository(db: Database):
    return UserRepository(db=db)

def get_password_hasher():
    return BcryptPasswordHasher(
        settings=settings
    )


def get_jwt_token_service() -> JWTService:
    return JWTService(settings=settings)

def get_departamento_repository(db: Database):
    return DepartamentoRepository(db=db)

def get_inquilino_repository(db: Database):
    return InquilinoRepository(db=db)

def get_cuota_repository(db: Database):
    return CuotaRepository(db=db)
