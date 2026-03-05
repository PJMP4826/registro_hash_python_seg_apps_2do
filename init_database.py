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

        query = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'cliente'
            );
        """

        db.execute(query=query)

        print("Schema de tablas creado")
    except Exception as e:
        print(f"Error creando el schema de tablas: {str(e)}")


if __name__ == "__main__":
    init_db()
