from pydantic import BaseModel


class CreateInquilinoWithUserRequest(BaseModel):
    nombre_completo: str
    email: str
    telefono: str
    password: str
    rol: str
    numero_departamento: int