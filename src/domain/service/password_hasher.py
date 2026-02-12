from abc import ABC, abstractmethod


class PasswordHasher(ABC):

    @abstractmethod
    def hash(self, password_txt: str):
        raise NotImplementedError()

    @abstractmethod
    def verify(self, password_txt: str, hashed_password: str):
        raise NotImplementedError()
