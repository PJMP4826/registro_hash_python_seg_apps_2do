from dataclasses import dataclass


@dataclass
class CreateInquilinoWithUserCommand:
    nombre_completo: str
    email: str
    telefono: str
    password: str
    rol: str
    numero_departamento: int