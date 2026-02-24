from pydantic import BaseModel

class AuthenticateUserRequest(BaseModel):
    email: str
    password_txt: str
