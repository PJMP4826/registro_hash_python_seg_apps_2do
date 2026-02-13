from dataclasses import dataclass

@dataclass()
class ChangePasswordDTO:
    email: str
    old_password_txt: str
    new_password_txt: str