from decimal import Decimal
from datetime import datetime
from ..enums.cuota_status import CuotaStatus


class Cuota:
    def __init__(
        self,
        id: str,
        inquilino_id: str,
        monto: Decimal,
        fecha: datetime,
        fecha_vencimiento: datetime,
        estado: CuotaStatus = CuotaStatus.PENDIENTE,
        monto_pagado: Decimal = Decimal("0.00"),
    ):
        self._id = id
        self._inquilino_id = inquilino_id
        self._monto = monto
        self._fecha = fecha
        self._fecha_vencimiento = fecha_vencimiento
        self._estado = estado
        self._monto_pagado = monto_pagado

    def apply_payment(self, amount: Decimal) -> None:

        if amount <= Decimal("0"):
            raise ValueError("El pago debe ser mayor a cero")

        new_total = self._monto_pagado + amount

        if new_total > self._monto:
            raise ValueError("El pago excede el monto")

        self._monto_pagado = new_total

        if self._monto_pagado == self._monto:
            self._estado = CuotaStatus.PAGADA
        else:
            self._estado = CuotaStatus.PARCIALMENTE_PAGADA

    def check_overdue(self) -> None:

        if self._estado == CuotaStatus.PAGADA:
            return

        if datetime.now() > self._fecha_vencimiento:
            self._estado = CuotaStatus.VENCIDA

    def is_paid(self) -> bool:
        return self._estado == CuotaStatus.PAGADA

    def remaining_balance(self) -> Decimal:
        return self._monto - self._monto_pagado
