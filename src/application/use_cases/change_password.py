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

    def execute(self, dto: ChangePasswordDTO):
        try:
            email = Email(dto.email)

            existing_password_hash = self.repo.get_password_hash_by_email(email)

            existing_password = Password.create_from_hash(existing_password_hash)

            verification_user = VerificationUser(
                password=existing_password,
                password_hasher=self.hasher
            )

            if not verification_user.verify_password(password_txt=dto.old_password_txt):
                raise ValueError("Contraseña invalida")

            new_password = Password.create_from_text(
                password_txt=dto.new_password_txt,
                hasher=self.hasher
            )

            self.repo.update_password(
                password_hash=new_password.hashed_value,
                email=email
            )

            return True
        except Exception as e:
            raise Exception(f"Error al cambiar la contraseña del usuario con email {email.value}: ", str(e))