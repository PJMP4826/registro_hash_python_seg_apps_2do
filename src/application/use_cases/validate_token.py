from src.domain.entities.token import TokenPayload
from src.domain.ports.jwt_service_port import TokenServicePort


class ValidateTokenUseCase:
    def __init__(self, token_service: TokenServicePort):
        self._token_service = token_service

    def execute(self, raw_token: str) -> TokenPayload:
        payload = self._token_service.validate(raw_token)

        return payload
