from dataclasses import dataclass
from src.infrastructure.config.logger import logger

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self.value:
            logger.debug("Se envio un email estar vacio")
            raise ValueError("El email no puede estar vacio")

        if not self._is_valid_format(self.value):
            logger.debug(f"Se envio un email invalido: {self.value}")
            raise ValueError(f"Email invalido: {self.value}")

        if len(self.value) > 255:
            logger.debug(f"Se envio un email muy grande: {self.value}")
            raise ValueError("El email no puede exceder los 255 caracteres")

    @staticmethod
    def _is_valid_format(email: str) -> bool:
        if not "@" in email:
            return False
        return True
