from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.enums.user_role import UserRole
from src.infrastructure.repository.user_repository import UserRepository
from src.application.dto.change_rol_dto import ChangeRolDTO
from src.domain.service.password_hasher import PasswordHasher
from src.domain.auth.verification_user import VerificationUser


class ChangeUserRol:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    def execute(self, dto: ChangeRolDTO) -> bool:
        try:
            # Validar el formato del email desde el dominio
            email = Email(dto.email)

            # Obtener el hash guardado en la BD
            existing_password_hash = self._get_password_hash_from_db(email=email.value)

            # Reconstruccion del Objeto de Valor de la contraseña
            existing_password = Password.create_from_hash(existing_password_hash)

            self._verify_password(
                existing_password=existing_password,
                password_txt=dto.password_txt
            )

            user_role = self._validate_user_rol_type(dto.rol)

            # Actualizar el registro en la base de datos
            self.repo.update_rol(
                rol_type=user_role,
                email=email.value
            )

            return True

        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error al cambiar el rol del usuario con email {dto.email}: {str(e)}")
        
    
    def _get_password_hash_from_db(self, email: str) -> str:
        try:
            existing_password_hash = self.repo.get_password_hash_by_email(email)
            if not existing_password_hash:
                raise ValueError("El usuario no existe")
            
            return existing_password_hash
        except ValueError as ve:
            raise ve
        

    def _verify_password(self, existing_password: Password, password_txt: str):
        try:
            verification_user = VerificationUser(
                password=existing_password,
                password_hasher=self.hasher
            )   
            if not verification_user.verify_password(password_txt=password_txt):
                raise ValueError("Contraseña actual inválida")
        except ValueError as ve:
            raise ve
        
    def _validate_user_rol_type(self, role_type: str) -> str:
        try:
            user_role = UserRole(role_type)
            return user_role.value
        except ValueError:
            valid_roles = ", ".join([role.value for role in UserRole])
            raise ValueError(f"El rol {role_type} no es válido. Roles permitidos: {str(valid_roles)}")
