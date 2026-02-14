from src.application.dto.change_password_dto import ChangePasswordDTO
from src.domain.auth.verification_user import VerificationUser
from src.domain.service.password_hasher import PasswordHasher
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.infrastructure.repository.user_repository import UserRepository


class ChangePassword:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    def execute(self, dto: ChangePasswordDTO) -> bool:
        try:
            # Validar el formato del email desde el dominio
            email = Email(dto.email)

            # Obtener el hash guardado en la BD
            existing_password_hash = self.repo.get_password_hash_by_email(email)
            if not existing_password_hash:
                raise ValueError("El usuario no existe")

            # Reconstruccion del Objeto de Valor de la contraseña
            existing_password = Password.create_from_hash(existing_password_hash)

            # Delegar verificación al servicio de dominio
            verification_user = VerificationUser(
                password=existing_password,
                password_hasher=self.hasher
            )

            # Validación de seguridad
            if not verification_user.verify_password(password_txt=dto.old_password_txt):
                raise ValueError("Contraseña actual inválida")

            # Creacion de la nueva contraseña
            new_password = Password.create_from_text(
                password_txt=dto.new_password_txt,
                hasher=self.hasher
            )

            # Actualizar el registro en la base de datos
            self.repo.update_password(
                password_hash=new_password.hashed_value,
                email=email
            )

            return True

        except ValueError as ve:
            raise ve
        except Exception as e:
            # dto.email en caso de que la variable email no se haya instanciado
            raise Exception(f"Error al cambiar la contraseña del usuario con email {dto.email}: {str(e)}")