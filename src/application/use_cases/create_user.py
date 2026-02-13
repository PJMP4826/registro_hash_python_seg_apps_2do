from src.infrastructure.repository.user_repository import UserRepository
from src.application.dto.create_user_dto import CreateUserDTO
from src.domain.service.password_hasher import PasswordHasher
from src.domain.service.password_hasher import PasswordHasher
from src.domain.entities.user import User
from src.domain.value_objects.email import Email
from src.domain.enums.user_role import UserRole

class CreateUser:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    def admin(self, dto: CreateUserDTO) -> bool:
        try:
            email = Email(dto.email)

            user = User.create(
                name=dto.name,
                email=email,
                password_txt=dto.password,
                role=UserRole.ADMIN,
                hasher=self.hasher
            )

            return self.repo.create_user(user=user)
        except Exception as e:
            raise Exception("Error al crear el usuario admin")