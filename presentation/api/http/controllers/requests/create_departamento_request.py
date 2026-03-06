from pydantic import BaseModel


class CreateDepartamentoRequest(BaseModel):
    piso: int
    num_departamento: int
    monto_renta: str
    status: str
