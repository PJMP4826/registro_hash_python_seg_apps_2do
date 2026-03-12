from src.domain.enums.user_role import UserRole
from src.domain.value_objects.email import Email
from src.infrastructure.config.logger import logger
from src.application.dto.change_rol_dto import ChangeRolDTO
from src.domain.service.password_hasher import PasswordHasher
from src.infrastructure.repository.user_repository import UserRepository


class ChangeUserRol:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self._repo = repo
        self._hasher = hasher

    def execute(self, dto: ChangeRolDTO) -> bool:
        try:
            # Validar el formato del email desde el dominio
            email = Email(dto.email)

            user = self._repo.get_user_by_email(email=email.value)

            if not user.verify_password(
                password_txt=dto.password_txt, password_hasher=self._hasher
            ):
                logger.warning(f"Contraseña '{dto.password_txt}' inválida para email {email.value}")
                raise ValueError("Contraseña actual inválida")

            user_role = self._validate_user_rol_type(dto.rol)

            # Actualizar el registro en la base de datos
            self._repo.update_rol(rol_type=user_role, email=email.value)

            return True

        except ValueError as ve:
            raise ve
        except Exception as e:
            logger.error(f"Error al cambiar el rol del usuario con email {dto.email}: {str(e)}")
            raise Exception(
                f"Error al cambiar el rol del usuario con email {dto.email}"
            )

    def _validate_user_rol_type(self, role_type: str) -> str:
        try:
            user_role = UserRole(role_type)
            return user_role.value
        except ValueError:
            valid_roles = ", ".join([role.value for role in UserRole])
            logger.error(f"El rol {role_type} no es válido. Roles permitidos: {str(valid_roles)}")
            raise ValueError(
                f"El rol {role_type} no es válido. Roles permitidos: {str(valid_roles)}"
            )
