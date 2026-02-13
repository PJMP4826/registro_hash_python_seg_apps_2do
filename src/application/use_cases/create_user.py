from src.infrastructure.repository.user_repository import UserRepository
from src.application.dto.create_user_dto import CreateUserDTO
from src.domain.service.password_hasher import PasswordHasher
from src.domain.entities.user import User
from src.domain.value_objects.email import Email
from src.domain.enums.user_role import UserRole


class CreateUser:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    def create_admin_user(self, dto: CreateUserDTO) -> bool:
        try:
            user_role = UserRole(dto.rol)
        except ValueError:
            valid_roles = ", ".join([role.value for role in UserRole])
            raise ValueError(f"El rol {dto.rol} no es válido. Roles permitidos: {str(valid_roles)}")

        email = Email(dto.email)

        user = User.create(
            name=dto.name,
            email=email,
            password_txt=dto.password,
            role=user_role,
            hasher=self.hasher
        )

        return self.repo.create_user(user=user)

    def create_client_user(self, dto: CreateUserDTO) -> bool:
        try:
            user_role = UserRole(dto.rol)
        except ValueError:
            valid_roles = ", ".join([role.value for role in UserRole])
            raise ValueError(f"El rol {dto.rol} no es válido. Roles permitidos: {str(valid_roles)}")

        email = Email(dto.email)

        user = User.create(
            name=dto.name,
            email=email,
            password_txt=dto.password,
            role=user_role,
            hasher=self.hasher
        )

        return self.repo.create_user(user=user)
