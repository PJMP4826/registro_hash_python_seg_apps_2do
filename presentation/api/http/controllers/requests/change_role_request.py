from pydantic import BaseModel

class ChangeRoleRequest(BaseModel):
    email: str
    password_txt: str
    role: str