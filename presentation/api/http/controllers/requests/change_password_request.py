from pydantic import BaseModel

class ChangePasswordRequest(BaseModel):
    email: str
    old_password_txt: str
    new_password_txt: str