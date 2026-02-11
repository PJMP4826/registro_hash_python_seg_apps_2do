from value_objects.email import Email
from value_objects.password import Password

class User:
    def __init__(self):
        self.name: str
        self._email: Email
        self._password: Password

    @property
    def email(self) -> str:
        return self._email.value
    
    @property
    def password(self) -> str:
        return self._password.value