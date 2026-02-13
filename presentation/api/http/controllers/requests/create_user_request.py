from pydantic.dataclasses import dataclass

@dataclass
class CreateUserRequest:
    name: str
    email: str
    password: str
    rol: str

