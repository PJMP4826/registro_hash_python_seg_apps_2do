from dataclasses import dataclass

@dataclass()
class AuthenticateUserDTO:
    email: str
    password_txt: str
