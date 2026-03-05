from decimal import Decimal
from typing import Optional
from src.domain.entities.departamento import Departamento
from src.domain.enums.departamento_status import DepartamentoStatus
from src.infrastructure.config.database import Database


class DepartamentoRepository:
    def __init__(self, db: Database):
        self._db = db

    def create(self, departamento: Departamento) -> int | None:
        if self.departamento_exist(departamento.num_departamento):
            raise ValueError(f"El departamento numero {departamento.num_departamento} ya existe") 
        
        query = """
            INSERT INTO departamentos (piso, num_departamento, monto_renta, status)
            VALUES (?, ?, ?, ?)
        """
        cursor = self._db.execute(
            query,
            (
                departamento.piso,
                departamento.num_departamento,
                float(departamento.monto_renta),
                departamento.status.value,
            ),
        )
        # devolver el id autoincremental recien creado
        return cursor.lastrowid

    def get_by_id(self, id_: int) -> Optional[Departamento]:
        query = """
            SELECT id, piso, num_departamento, monto_renta, status
            FROM departamentos
            WHERE id = ?
        """
        row = self._db.execute_query_fetchone(query, (id_,))
        if not row:
            return None

        return Departamento(
            id=int(row[0]),
            piso=int(row[1]),
            num_departamento=int(row[2]),
            monto_renta=Decimal(str(row[3])),
            status=DepartamentoStatus(row[4]),
        )
    
    def departamento_exist(self, num_departamento: int) -> bool:
        query = "SELECT COUNT(*) as count FROM departamentos WHERE num_departamento = ?"
        result = self._db.execute_query_fetchone(query, (str(num_departamento),))
        return result[0] > 0 # type: ignore

    def list_available(self) -> list[Departamento]:
        query = """
            SELECT id, piso, num_departamento, monto_renta, status
            FROM departamentos
            WHERE status = 'disponible'
        """
        rows = self._db.execute_query_fetchall(query)
        return [
            Departamento(
                id=int(r[0]),
                piso=int(r[1]),
                num_departamento=int(r[2]),
                monto_renta=Decimal(str(r[3])),
                status=DepartamentoStatus(r[4]),
            )
            for r in rows
        ]

    def update_status(self, id_: int, status: DepartamentoStatus) -> None:
        query = "UPDATE departamentos SET status = ? WHERE id = ?"
        self._db.execute(query, (status.value, id_))
