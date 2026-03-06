from dataclasses import dataclass

@dataclass
class CreateUserAdminCommand():
    name: str
    email: str
    password: str