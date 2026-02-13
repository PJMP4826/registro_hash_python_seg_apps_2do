from src.infrastructure.config.database import Database
from src.infrastructure.repository.user_repository import UserRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher

def get_db_session() -> Database:
    db = Database()
    db.connect("../test_db.db")
    return db

def get_user_repository(db: Database):
    return UserRepository(db=db)

def get_password_hasher():
    return BcryptPasswordHasher()