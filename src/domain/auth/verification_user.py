from dataclasses import dataclass

from src.domain.service.password_hasher import PasswordHasher
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password


@dataclass
class VerificationUser:
    password: Password
    password_hasher: PasswordHasher

    def verify_password(self, password_txt: str):
        return self.password.verify(password_txt=password_txt, hasher=self.password_hasher)