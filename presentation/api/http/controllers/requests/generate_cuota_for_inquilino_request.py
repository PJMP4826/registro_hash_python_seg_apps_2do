from pydantic import BaseModel

class GenerateCuotaForInquilinoRequest(BaseModel):
    email: str
    year: int
    month: int
    dia_vencimiento: int = 5
