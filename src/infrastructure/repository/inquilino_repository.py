from typing import Optional
from src.domain.entities.inquilino import Inquilino
from src.infrastructure.config.database import Database

class InquilinoRepository:
    def __init__(self, db: Database):
        self._db = db

    def create(self, inquilino: Inquilino) -> int | None:
        query = """
            INSERT INTO inquilinos (nombre_completo, telefono, estatus, departamento_id)
            VALUES (?, ?, ?, ?)
        """
        cursor = self._db.execute( 
            query,
            (
                inquilino.nombre_completo,
                inquilino.telefono,
                1 if inquilino.estatus else 0,
                inquilino.departamento_id,
            ),
        )
        return cursor.lastrowid

    def get_by_id(self, id_: int) -> Optional[Inquilino]:
        query = """
            SELECT id, nombre_completo, telefono, departamento_id, estatus
            FROM inquilinos
            WHERE id = ?
        """
        row = self._db.execute_query_fetchone(query, (id_,)) 
        if not row:
            return None

        return Inquilino(
            id=row[0],
            nombre_completo=row[1],
            telefono=row[2],
            departamento_id=row[3],
            estatus=bool(row[4]),
        )

    def get_by_departamento_id(self, departamento_id: int) -> Optional[Inquilino]:
        query = """
            SELECT id, nombre_completo, telefono, departamento_id, estatus
            FROM inquilinos
            WHERE departamento_id = ?
        """
        row = self._db.execute_query_fetchone(query, (departamento_id,)) 
        if not row:
            return None
        return Inquilino(
            id=row[0],
            nombre_completo=row[1],
            telefono=row[2],
            departamento_id=row[3],
            estatus=bool(row[4]),
        )

    def list_active(self) -> list[Inquilino]:
        query = """
            SELECT id, nombre_completo, telefono, departamento_id, estatus
            FROM inquilinos
            WHERE estatus = 1
        """
        rows = self._db.execute_query_fetchall(query) 
        return [
            Inquilino(
                id=r[0],
                nombre_completo=r[1],
                telefono=r[2],
                departamento_id=r[3],
                estatus=bool(r[4]),
            )
            for r in rows
        ]