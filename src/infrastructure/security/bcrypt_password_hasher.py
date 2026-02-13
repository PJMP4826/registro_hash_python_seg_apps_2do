import bcrypt
from src.domain.service.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def __init__(self, rounds: int = 12):
        self.rounds = rounds

    def hash(self, plain_password: str) -> str:
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
