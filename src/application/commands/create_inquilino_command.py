from dataclasses import dataclass


@dataclass
class CreateInquilinoCommand:
    nombre_completo: str
    telefono: str
    numero_departamento: int
