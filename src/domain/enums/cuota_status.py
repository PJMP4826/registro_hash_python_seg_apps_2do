from enum import Enum

class CuotaStatus(Enum):
    PENDIENTE = "pendiente"
    PARCIALMENTE_PAGADA = "parcialmente_pagada"
    PAGADA = "pagada"
    VENCIDA = "vencida"