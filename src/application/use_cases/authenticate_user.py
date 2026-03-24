import re
from src.domain.entities.user import User
from datetime import datetime, timedelta
from src.domain.value_objects.email import Email
from src.infrastructure.config.logger import logger
from src.infrastructure.repository.user_repository import UserRepository
from src.application.dto.authenticate_user_dto import AuthenticateUserDTO
from src.domain.service.password_hasher import PasswordHasher
from src.domain.entities.token import TokenPayload
from src.domain.value_objects.auth_token import AuthToken
from src.domain.ports.jwt_service_port import TokenServicePort
from src.infrastructure.config.settings import Settings


class AuthenticateUser:
    def __init__(
        self,
        repo: UserRepository,
        hasher: PasswordHasher,
        token_service: TokenServicePort,
        settings: Settings,
    ):
        self._repo = repo
        self._hasher = hasher
        self._token_service = token_service
        self._settings = settings

    _EMAIL_BASIC_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def execute(self, dto: AuthenticateUserDTO) -> AuthToken:
        try:
            # Validar el formato del email desde el dominio
            email = Email(dto.email)

            user = self._repo.get_user_by_email(email=email.value)

            if not user:
                logger.warning(f"Usuario con email {self.mask_email(email.value)} no encontrado")
                raise ValueError("Usuario no encontrado")

            if not user.verify_password( # type: ignore
                password_txt=dto.password_txt, password_hasher=self._hasher
            ):
                logger.warning(f"Contraseña actual inválida")
                raise ValueError("Contraseña actual inválida")

            logger.info(f"Usuario con email {self.mask_email(email.value)} autenticado exitosamente")
            return self._generate_jwt_token(user=user)

        except ValueError as ve:
            raise ve
        except Exception as e:
            logger.error(f"Error al autenticar usuario con email {self.mask_email(dto.email)}: {str(e)}")
            raise Exception(
                f"Error al autenticar usuario con email {dto.email}"
            )

    def _generate_jwt_token(self, user: User) -> AuthToken:
        expiration_time = datetime.now() + timedelta(
            minutes=self._settings.jwt_expires_in_minutes
        )

        payload = TokenPayload(
            subject=user.uuid,
            claim={"email": user.email.value, "role": user.role.value},
            expires_at=expiration_time,
            iat=datetime.now(),
        )

        token = self._token_service.generate(payload=payload)

        return token
    
    def mask_email(self, email: str) -> str:
        """
        Ejemplos:
        - admin@system.local -> a***n@s****m.local
        - edna@gmail.com     -> e**a@g***l.com
        """
        if not email:
            return "***@***"

        value = email.strip().lower()

        # si no parece email, no devolvemos el valor original para evitar fuga de datos.
        if not self._EMAIL_BASIC_RE.match(value):
            return "***@***"

        local, domain = value.split("@", 1)

        def mask_segment(text: str, keep_start: int = 1, keep_end: int = 1) -> str:
            if len(text) <= keep_start + keep_end:
                return "*" * len(text)
            middle = "*" * (len(text) - keep_start - keep_end)
            return f"{text[:keep_start]}{middle}{text[-keep_end:]}"

        # dominio: separa nombre y tld para conservar trazabilidad mínima (ej: .com, .local)
        if "." in domain:
            domain_name, tld = domain.rsplit(".", 1)
            masked_domain = f"{mask_segment(domain_name)}.{tld}"
        else:
            masked_domain = mask_segment(domain)

        return f"{mask_segment(local)}@{masked_domain}"
