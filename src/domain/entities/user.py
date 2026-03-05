import uuid
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
    ):
        self._uuid = uuid
        self._name = name
        self._email = email
        self._password = password
        self._role = role

    # exponer propiedades read-only en python
    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def email(self) -> Email:
        return self._email

    @property
    def role(self) -> UserRole:
        return self._role

    @property
    def password(self) -> Password:
        return self._password

    def verify_password(self, password_txt: str, password_hasher: PasswordHasher) -> bool:
        return self._password.verify(password_txt, password_hasher)

    def change_password(
        self,
        old_password_txt: str,
        new_password_txt: str,
        password_hasher: PasswordHasher,
    ) -> None:

        if not self._password.verify(old_password_txt, password_hasher):
            raise ValueError("Invalid current password")

        self._password = Password.create_from_text(
            password_txt=new_password_txt, hasher=password_hasher
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

        return {
            "uuid": self._uuid,
            "name": self._name,
            "email": str(self._email),
            "password": self._password.hashed_value,
            "role": self._role.value,
        }

    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            uuid=data["uuid"],
            name=data["name"],
            email=Email(data["email"]),
            password=Password.create_from_hash(data["password"]),
            role=UserRole(data["role"]),
        )
