import uuid
from src.domain.service.password_hasher import PasswordHasher
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.enums.user_role import UserRole
from dataclasses import dataclass


@dataclass()
class User:
    uuid: str
    name: str
    email: Email
    password: Password
    role: UserRole

    # en este puento User ya tiene carga el hash de la password desde DB en password.hashed_value
    def verify_password(self, password_txt: str, password_hasher: PasswordHasher):
        return self.password.verify(password_txt, password_hasher)

    def change_password(
        self, old_password_txt: str, new_password: str, password_hasher: PasswordHasher
    ) -> Password:
        if not self.password.verify(
            password_txt=old_password_txt, hasher=password_hasher
        ):
            raise ValueError("Contraseña actual inválida")

        self.password = Password.create_from_text(
            password_txt=new_password, hasher=password_hasher
        )

    @classmethod
    def create(
        cls,
        name: str,
        email: Email,
        password_txt: str,
        role: UserRole,
        hasher: PasswordHasher,
    ):

        return cls(
            uuid=str(uuid.uuid4()),
            name=name,
            email=email,
            password=Password.create_from_text(password_txt, hasher),
            role=role,
        )

    def to_dict(self) -> dict:
        """convierte a diccionario para persistencia"""
        return {
            "uuid": self.uuid,
            "name": str(self.name),
            "email": str(self.email),
            "password": self.password.hashed_value,
            "role": self.role.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            uuid=data["uuid"],
            name=data["name"],
            email=Email(data["email"]),
            password=Password.create_from_hash(data["password"]),
            role=UserRole(data["role"]),
        )
