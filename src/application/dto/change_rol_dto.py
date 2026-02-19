from dataclasses import dataclass

@dataclass()
class ChangeRolDTO:
    email: str
    password_txt: str
    rol: str