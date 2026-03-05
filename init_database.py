from src.bootstrap.providers import BASE_DIR
from src.infrastructure.config.settings import settings
from src.infrastructure.config.database import Database

db = Database()


def init_db():
    try:

        database_path = BASE_DIR / settings.database_name
        print(database_path)

        created = db.create_database(db_name=database_path)

        if created:
            print(
                f"Base de datos SQLite {settings.database_name} Creada exitosamente en {database_path}"
            )

        create_tables_schema(db_name=database_path)

    except Exception as e:
        print(f"Error creando la base de datos SQLite: {str(e)}")


def create_tables_schema(db_name: str):
    try:
        db.connect(db_name=db_name)

        queries = [
            "PRAGMA foreign_keys = ON;",

            """ 
            CREATE TABLE departamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                piso TEXT NOT NULL,
                num_departamento INTEGER NOT NULL,
                monto_renta NUMERIC NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('ocupado','disponible'))
            );
            """,

            """
            CREATE TABLE inquilinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_completo TEXT NOT NULL,
                telefono TEXT NOT NULL,
                estatus INTEGER NOT NULL CHECK (estatus IN (0,1)),
                departamento_id INTEGER NOT NULL UNIQUE,
                FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
            );
            """,

            """
            CREATE TABLE cuotas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inquilino_id INTEGER NOT NULL,
                monto NUMERIC NOT NULL,
                fecha TEXT NOT NULL,
                fecha_vencimiento TEXT NOT NULL,
                estado TEXT NOT NULL CHECK (
                    estado IN ('pendiente','vencida','pagada','parcialmente_pagada')
                ),
                FOREIGN KEY (inquilino_id) REFERENCES inquilinos(id)
            );
            """,

            """
            CREATE TABLE pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monto NUMERIC NOT NULL,
                fecha TEXT NOT NULL,
                cuota_id INTEGER NOT NULL,
                FOREIGN KEY (cuota_id) REFERENCES cuotas(id)
            );
            """,

            """
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inquilino_id INTEGER,
                uuid TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('admin','cliente')),
                FOREIGN KEY (inquilino_id) REFERENCES inquilinos(id)
            );
            """
        ]

        for query in queries:
            db.execute(query=query)

        print("Schema de tablas creado")
    except Exception as e:
        print(f"Error creando el schema de tablas: {str(e)}")


if __name__ == "__main__":
    init_db()
