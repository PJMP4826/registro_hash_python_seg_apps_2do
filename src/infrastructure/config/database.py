import sqlite3
from sqlite3 import Connection, Cursor
from typing import Optional, Any, Sequence


class Database:
    def __init__(self) -> None:
        self._connection: Optional[Connection] = None

    @property
    def connection(self) -> Optional[Connection]:
        return self._connection

    @staticmethod
    def create_database(db_name: str) -> bool:
        sqlite_connection: Optional[Connection] = None

        try:
            sqlite_connection = sqlite3.connect(db_name)
            return True
        except sqlite3.Error as error:
            print("Error occurred:", error)
            return False
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def connect(self, db_name: str) -> None:
        try:
            self._connection = sqlite3.connect(db_name)
        except Exception as e:
            raise Exception(f"Error connecting to db: {db_name}, Error: {str(e)}")

    def close(self) -> None:
        try:
            if self._connection:
                self._connection.close()
                self._connection = None
        except Exception as e:
            raise Exception(f"Error closing connection: {str(e)}")

    def has_tables(self) -> bool:
        tables = self.execute_query_fetchall(
            "SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
        )
        return len(tables) > 0

    def execute(self, query: str, params: Optional[Sequence[Any]] = None) -> Cursor:
        if not self._connection:
            raise RuntimeError("Database not connected")

        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params or ())
            self._connection.commit()
            return cursor
        except Exception as e:
            raise Exception(f"Error executing query: {query}, Error: {str(e)}")

    def execute_query_fetchall(
        self, query: str, params: Optional[Sequence[Any]] = None
    ) -> list[tuple[Any, ...]]:
        if not self._connection:
            raise RuntimeError("Database not connected")

        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error executing query: {query}, Error: {str(e)}")

    def execute_query_fetchmany(
        self, query: str, params: Optional[Sequence[Any]] = None
    ) -> list[tuple[Any, ...]]:
        if not self._connection:
            raise RuntimeError("Database not connected")

        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchmany()
        except Exception as e:
            raise Exception(f"Error executing query: {query}, Error: {str(e)}")

    def execute_query_fetchone(
        self, query: str, params: Optional[Sequence[Any]] = None
    ) -> Optional[tuple[Any, ...]]:
        if not self._connection:
            raise RuntimeError("Database not connected")

        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Exception as e:
            raise Exception(f"Error executing query: {query}, Error: {str(e)}")