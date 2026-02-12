from domain.service.password_hasher import PasswordHasher
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from dataclasses import dataclass

@dataclass()
class User:
    name: str
    email: Email
    password: Password
    password_hasher: PasswordHasher

    def verify_password(self, password: str):
        return self.password.verify(password, self.password_hasher)

    def to_dict(self) -> dict:
        """convierte a diccionario para persistencia"""
        return {
            'name': str(self.name),
            'email': str(self.email),
            'password': self.password.hashed_value
        }

    @classmethod
    def from_dict(cls, data: dict, password_hasher: PasswordHasher) -> 'User':
        return cls(
            name=data['name'],
            email=Email(data['email']),
            password=Password.from_hash(data['password']),
        )