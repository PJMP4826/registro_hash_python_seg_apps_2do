from src.infrastructure.config.database import Database
from src.infrastructure.repository.user_repository import UserRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "test_db.db"

def get_db_session() -> Database:
    db = Database()
    db.connect(str(DB_PATH))
    return db

def get_user_repository(db: Database):
    return UserRepository(db=db)

def get_password_hasher():
    return BcryptPasswordHasher()