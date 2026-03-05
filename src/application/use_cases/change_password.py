from src.application.dto.change_password_dto import ChangePasswordDTO
from src.domain.service.password_hasher import PasswordHasher
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.infrastructure.repository.user_repository import UserRepository


class ChangePassword:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self._repo = repo
        self._hasher = hasher

    def execute(self, dto: ChangePasswordDTO) -> bool:
        try:
            # Validar el formato del email desde el dominio
            email = Email(dto.email)

            user = self._repo.get_user_by_email(email=email.value)

            # Creacion de la nueva contraseña
            user.change_password(
                new_password_txt=dto.new_password_txt,
                old_password_txt=dto.old_password_txt,
                password_hasher=self._hasher,
            )

            # Actualizar el registro en la base de datos
            self._repo.update_password(
                password_hash=user.password.hashed_value, email=email
            )

            return True

        except ValueError as ve:
            raise ve
        except Exception as e:
            # dto.email en caso de que la variable email no se haya instanciado
            raise Exception(
                f"Error al cambiar la contraseña del usuario con email {dto.email}: {str(e)}"
            )
