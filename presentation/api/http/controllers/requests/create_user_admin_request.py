from pydantic import BaseModel

class CreateUserAdminRequest(BaseModel):
    name: str
    email: str
    password: str