from src.domain.entities.token import TokenPayload
from src.domain.value_objects.auth_token import AuthToken
from abc import ABC, abstractmethod

class TokenServicePort(ABC):

    @abstractmethod
    def generate(self, payload: TokenPayload) -> AuthToken:
        raise NotImplementedError
    
    def validate(self, token: str) -> TokenPayload:
        raise NotImplementedError
    
    # def refresh(self)
