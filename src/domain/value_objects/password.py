import re
from dataclasses import dataclass
from src.domain.service.password_hasher import PasswordHasher
from src.infrastructure.config.logger import logger


@dataclass(frozen=True)
class Password:
    hashed_value: str

    def __post_init__(self):
        if not self.hashed_value:
            logger.debug("El hash del password esta vacío")
            raise ValueError("El hash no puede estar vacio")

    @classmethod
    def create_from_text(cls, password_txt: str, hasher: PasswordHasher) -> "Password":
        cls._validate_strength(password=password_txt)
        hashed = hasher.hash(password_txt)
        return cls(hashed)

    @classmethod
    def create_from_hash(cls, hashed_password: str) -> "Password":
        return cls(hashed_password)

    def verify(self, password_txt: str, hasher: PasswordHasher) -> bool:
        return hasher.verify(password_txt, hashed_password=self.hashed_value)

    @staticmethod
    def _validate_strength(password: str) -> None:
        """Valida la fortaleza de la contraseña"""
        if len(password) < 8:
            logger.debug(f"Se envio una contraseña menor a 8 caracteres")
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        if len(password) > 10:
            logger.debug(f"Se envio una contraseña mayor a 10 caracteres")
            raise ValueError("La contraseña no puede exceder los 10 caracteres")

        if not re.search(r'[A-Z]', password):
            logger.debug(f"Se envio una contraseña sin mayúsculas")
            raise ValueError("La contraseña debe contener al menos una mayúscula")

        if not re.search(r'[a-z]', password):
            logger.debug(f"Se envio una contraseña sin minusculas")
            raise ValueError("La contraseña debe contener al menos una minúscula")

        if not re.search(r'\d', password):
            logger.debug(f"Se envio una contraseña sin numeros")
            raise ValueError("La contraseña debe contener al menos un número")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            logger.debug(f"Se envio una contraseña sin un carácter especial")
            raise ValueError("La contraseña debe contener al menos un carácter especial")
