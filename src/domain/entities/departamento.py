from ..enums.departamento_status import DepartamentoStatus
from decimal import Decimal


class Departamento:
    def __init__(
        self,
        id: str,
        piso: int,
        num_departamento: str,
        monto_renta: Decimal,
        status: DepartamentoStatus = DepartamentoStatus.DISPONIBLE,
    ):
        self._id = id
        self._piso = piso
        self._num_departamento = num_departamento
        self._monto_renta = monto_renta
        self._status = status

    @property
    def id(self) -> str:
        return self._id

    @property
    def status(self) -> DepartamentoStatus:
        return self._status

    def mark_as_occupied(self) -> None:
        if self._status == DepartamentoStatus.OCUPADO:
            raise ValueError("Department already occupied")

        self._status = DepartamentoStatus.OCUPADO

    def mark_as_available(self) -> None:
        self._status = DepartamentoStatus.DISPONIBLE

    def is_available(self) -> bool:
        return self._status == DepartamentoStatus.DISPONIBLE
