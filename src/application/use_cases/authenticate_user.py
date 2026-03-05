from datetime import datetime, timedelta
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.enums.user_role import UserRole
from src.infrastructure.repository.user_repository import UserRepository
from src.application.dto.authenticate_user_dto import AuthenticateUserDTO
from src.domain.service.password_hasher import PasswordHasher
from src.domain.auth.verification_user import VerificationUser
from src.domain.entities.token import TokenPayload
from src.domain.value_objects.auth_token import AuthToken
from src.domain.ports.jwt_service_port import TokenServicePort
from src.infrastructure.config.settings import Settings


class AuthenticateUser:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher, token_service: TokenServicePort, settings: Settings):
        self._repo = repo
        self._hasher = hasher
        self._token_service = token_service
        self._settings = settings

    def execute(self, dto: AuthenticateUserDTO) -> AuthToken:
        try:
            # Validar el formato del email desde el dominio
            email = Email(dto.email)

            # Obtener el hash guardado en la BD
            existing_password_hash = self._get_password_hash_from_db(email=email.value)

            # Reconstruccion del Objeto de Valor de la contraseña
            existing_password = Password.create_from_hash(existing_password_hash)

            user = self._repo.get_user_by_email(email=email.value)

            self._verify_password(
                existing_password=existing_password,
                password_txt=dto.password_txt
            )

            return self._generate_jwt_token(user_data=user)

        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error al autenticar usuario con email {dto.email}: {str(e)}")
        
    
    def _get_password_hash_from_db(self, email: str) -> str:
        try:
            existing_password_hash = self._repo.get_password_hash_by_email(email)
            if not existing_password_hash:
                raise ValueError("El usuario no existe")
            
            return existing_password_hash
        except ValueError as ve:
            raise ve
        

    def _verify_password(self, existing_password: Password, password_txt: str):
        try:
            verification_user = VerificationUser(
                password=existing_password,
                password_hasher=self._hasher
            )   
            if not verification_user.verify_password(password_txt=password_txt):
                raise ValueError("Contraseña actual inválida")
            return True

        except ValueError as ve:
            raise ve
        
    def _generate_jwt_token(self, user_data: dict[str, str]) -> AuthToken:
            expiration_time = datetime.now() + timedelta(minutes=self._settings.jwt_expires_in_minutes)


            payload = TokenPayload(
                subject=user_data.get("uuid"),
                claim={
                    "email": user_data.get("email"),
                    "role": user_data.get("role")
                },
                expires_at=expiration_time,
                iat=datetime.now()
            )

            token = self._token_service.generate(payload=payload)

            return token

