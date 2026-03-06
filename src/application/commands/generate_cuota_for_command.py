from dataclasses import dataclass


@dataclass
class GenerateCuotaForInquilinoCommand:
    email: str
    year: int
    month: int
    dia_vencimiento: int = 5