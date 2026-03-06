from dataclasses import dataclass


@dataclass
class CreateDepartamentoCommand:
    piso: int
    num_departamento: int
    monto_renta: str
    status: str
