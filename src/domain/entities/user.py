import uuid
from typing import Any
from src.domain.service.password_hasher import PasswordHasher
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.enums.user_role import UserRole


class User:
    def __init__(
        self,
        uuid: str,
        name: str,
        email: Email,
        password: Password,
        role: UserRole,
        inquilino_id: int | None = None
    ):
        self._uuid = uuid
        self._name = name
        self._email = email
        self._password = password
        self._role = role
        self._inquilino_id = inquilino_id

        self._validate_integrity()

    # exponer propiedades read-only en python
    @property
    def uuid(self) -> str:
        return self._uuid
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> Email:
        return self._email

    @property
    def role(self) -> UserRole:
        return self._role

    @property
    def password(self) -> Password:
        return self._password
    
    @property
    def inquilino_id(self) -> int | None:
        return self._inquilino_id

    def verify_password(self, password_txt: str, password_hasher: PasswordHasher) -> bool:
        return self._password.verify(password_txt, password_hasher)

    def change_password(
        self,
        old_password_txt: str,
        new_password_txt: str,
        password_hasher: PasswordHasher,
    ) -> None:

        if not self._password.verify(old_password_txt, password_hasher):
            raise ValueError("Contraseña actual invalida")

        self._password = Password.create_from_text(
            password_txt=new_password_txt, hasher=password_hasher
        )

    def is_admin(self) -> bool:
        return self.role.value == "admin"
    
    def is_client(self) -> bool:
        return self.role.value == "cliente"
    
    def is_linked_to_inquilino(self) -> bool:
        return self._inquilino_id is not None
    
    def _validate_integrity(self):
        if self._role == UserRole.CLIENTE and self._inquilino_id is None:
            raise ValueError("Un cliente debe ser inquilino de un departamento")

        if self._role == UserRole.ADMIN and self._inquilino_id is not None:
            raise ValueError("El Administrador no puede tomar un departamento")

    @classmethod
    def create(
        cls,
        name: str,
        email: Email,
        password_txt: str,
        role: UserRole,
        hasher: PasswordHasher,
        inquilino_id: int | None = None
    ):

        return cls(
            uuid=str(uuid.uuid4()),
            name=name,
            email=email,
            password=Password.create_from_text(password_txt, hasher),
            role=role,
            inquilino_id=inquilino_id
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": self._uuid,
            "name": self._name,
            "email": str(self._email),
            "password": self._password.hashed_value,
            "role": self._role.value,
            "inquilino_id": str(self._inquilino_id) if self._inquilino_id else None
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]):

        return cls(
            uuid=data["uuid"],
            name=data["name"],
            email=Email(data["email"]),
            password=Password.create_from_hash(data["password"]),
            role=UserRole(data["role"]),
            inquilino_id=(data["inquilino_id"]) if data["inquilino_id"] else None
        )
