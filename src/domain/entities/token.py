from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TokenPayload:
    subject: str
    claim: dict
    expires_at: datetime
    iat: datetime

    def get_claim(self, key: str) -> str:
        return self.claim.get(key)
