import sqlite3
from sqlite3 import Connection
from typing import Optional, Any


class Database:
    def __init__(self):
        self._connection: Optional[Connection] = None

    @property
    def connection(self) -> Optional[Connection]:
        return self._connection

    @staticmethod
    def create_database(db_name: str) -> bool:
        try:
            sqliteConnection = sqlite3.connect(db_name)

            return True
        except sqlite3.Error as error:
            print("Error occurred:", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def connect(self, db_name: str) -> Connection:
        try:
            self._connection = sqlite3.connect(db_name)
        except Exception as e:
            raise Exception(f"Error al conectar a la db: {db_name}, Error: {str(e)}")

    def close(self):
        try:
            if self.connection:
                self.connection.close()
                self._connection = None
        except Exception as e:
            raise Exception(f"Error al cerrar la connection: {str(e)}")

    def has_tables(self) -> bool:
        try:
            tables = self.execute_query(
                "SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
            )
            return len(tables) > 0
        except Exception as e:
            raise e

    def execute_query(self, query) -> list[Any]:
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al ejecutar la consulta: {query}, Error: {str(e)}")
