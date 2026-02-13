from pydantic.dataclasses import dataclass

@dataclass
class CreateUserDTO:
    name: str
    email: str
    password: str
    rol: str

