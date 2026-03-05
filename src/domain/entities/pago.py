from decimal import Decimal
from datetime import datetime


class Pago:

    def __init__(
        self,
        id: int,
        cuota_id: str,
        inquilino_id: str,
        amount: Decimal,
        payment_date: datetime,
    ):
        self._id = id
        self._cuota_id = cuota_id
        self._inquilino_id = inquilino_id
        self._amount = amount
        self._payment_date = payment_date

        self._validate()

    def _validate(self):
        if self._amount <= Decimal("0"):
            raise ValueError("El pago debe ser mayor a cero")

    @property
    def id(self) -> int:
        return self._id

    @property
    def cuota_id(self) -> str:
        return self._cuota_id

    @property
    def inquilino_id(self) -> str:
        return self._inquilino_id

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def payment_date(self) -> datetime:
        return self._payment_date
