from datetime import datetime, timedelta
from src.domain.value_objects.email import Email
from src.domain.entities.user import User
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

    def execute(self, dto: AuthenticateUserDTO) -> AuthToken:
        try:
            # Validar el formato del email desde el dominio
            email = Email(dto.email)

            user = self._repo.get_user_by_email(email=email.value)

            if not user.verify_password(
                password_txt=dto.password_txt, password_hasher=self._hasher
            ):
                raise ValueError("Contraseña actual inválida")

            return self._generate_jwt_token(user=user)

        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(
                f"Error al autenticar usuario con email {dto.email}: {str(e)}"
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
