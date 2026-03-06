from decimal import Decimal
from datetime import datetime
from typing import Optional
from src.domain.entities.couta import Cuota
from src.domain.enums.cuota_status import CuotaStatus
from src.infrastructure.config.database import Database


class CuotaRepository:
    def __init__(self, db: Database):
        self._db = db

    def create(self, cuota: Cuota) -> int | None:
        query = """
            INSERT INTO cuotas (
                inquilino_id, monto_esperado, monto_pagado,
                fecha, fecha_vencimiento, estado
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor = self._db.execute(
            query,
            (
                int(cuota.inquilino_id),
                float(cuota.monto),
                float(cuota.monto_pagado),
                cuota.fecha.isoformat(),
                cuota.fecha_vencimiento.isoformat(),
                cuota.estado.value,
            ),
        )
        return cursor.lastrowid

    def get_by_id(self, id_: int) -> Optional[Cuota]:
        query = """
            SELECT id, inquilino_id, monto_esperado, monto_pagado,
                   fecha, fecha_vencimiento, estado
            FROM cuotas
            WHERE id = ?
        """
        row = self._db.execute_query_fetchone(query, (id_,))
        if not row:
            return None

        return Cuota(
            id=str(row[0]),
            inquilino_id=str(row[1]),
            monto=Decimal(str(row[2])),
            monto_pagado=Decimal(str(row[3])),
            fecha=datetime.fromisoformat(row[4]),
            fecha_vencimiento=datetime.fromisoformat(row[5]),
            estado=CuotaStatus(row[6]),
        )

    def list_by_inquilino(self, inquilino_id: int) -> list[Cuota]:
        query = """
            SELECT id, inquilino_id, monto_esperado, monto_pagado,
                   fecha, fecha_vencimiento, estado
            FROM cuotas
            WHERE inquilino_id = ?
        """
        rows = self._db.execute_query_fetchall(query, (inquilino_id,))
        return [
            Cuota(
                id=str(r[0]),
                inquilino_id=str(r[1]),
                monto=Decimal(str(r[2])),
                monto_pagado=Decimal(str(r[3])),
                fecha=datetime.fromisoformat(r[4]),
                fecha_vencimiento=datetime.fromisoformat(r[5]),
                estado=CuotaStatus(r[6]),
            )
            for r in rows
        ]

    def update(self, cuota: Cuota) -> None:
        query = """
            UPDATE cuotas
            SET monto_esperado = ?, monto_pagado = ?, fecha = ?,
                fecha_vencimiento = ?, estado = ?
            WHERE id = ?
        """
        self._db.execute(
            query,
            (
                float(cuota.monto),
                float(cuota.monto_pagado),
                cuota.fecha.isoformat(),
                cuota.fecha_vencimiento.isoformat(),
                cuota.estado.value,
                int(cuota.id),
            ),
        )
