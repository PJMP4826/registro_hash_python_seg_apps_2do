from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from src.application.commands.generate_cuota_for_command import (
    GenerateCuotaForInquilinoCommand,
)
from src.domain.entities.couta import Cuota
from src.domain.enums.cuota_status import CuotaStatus
from src.infrastructure.repository.cuota_repository import CuotaRepository
from src.infrastructure.repository.departamento_repository import DepartamentoRepository
from src.infrastructure.repository.inquilino_repository import InquilinoRepository


class GenerateCuotaForInquilino:
    def __init__(
        self,
        inquilino_repo: InquilinoRepository,
        departamento_repo: DepartamentoRepository,
        cuota_repo: CuotaRepository,
    ) -> None:
        self._inquilino_repo = inquilino_repo
        self._departamento_repo = departamento_repo
        self._cuota_repo = cuota_repo

    def execute(self, command: GenerateCuotaForInquilinoCommand) -> int | None:
        
        # validar inquilino existe y esta activo
        inquilino = self._inquilino_repo.get_by_email(command.email)
        if not inquilino:
            raise ValueError(f"No existe el inquilino con email {command.email}")

        if not inquilino.is_active():
            raise ValueError("No se puede generar cuota para un inquilino inactivo")

        # obtener departamento para el monto de la renta
        departamento = self._departamento_repo.get_by_id(inquilino.departamento_id)
        if not departamento:
            raise ValueError("El inquilino no tiene un departamento asociado válido")

        # evitar cuota duplicada para el mismo mes/año
        cuotas_existentes = self._cuota_repo.list_by_inquilino(inquilino.id)
        print("cuotas_existentes: ", [cuota.fecha for cuota in cuotas_existentes])
        for c in cuotas_existentes:
            if c.fecha.year == command.year and c.fecha.month == command.month:
                raise ValueError(
                    f"Ya existe una cuota para el inquilino para el {c.fecha.day}/{c.fecha.month}/{c.fecha.year}"
                )

        # fechas: inicio del periodo y vencimiento
        _, ultimo_dia = monthrange(command.year, command.month)
        dia_venc = min(command.dia_vencimiento, ultimo_dia)
        fecha_emision = datetime(command.year, command.month, 1)
        fecha_vencimiento = datetime(command.year, command.month, dia_venc)

        cuota = Cuota(
            id="0",
            inquilino_id=str(inquilino.id),
            monto=departamento.monto_renta,
            fecha=fecha_emision,
            fecha_vencimiento=fecha_vencimiento,
            estado=CuotaStatus.PENDIENTE,
            monto_pagado=Decimal("0.00"),
        )

        return self._cuota_repo.create(cuota)