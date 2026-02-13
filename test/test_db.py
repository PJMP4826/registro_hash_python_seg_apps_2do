from src.infrastructure.config.database import Database

db = Database()

# crear db
db.create_database('../test_db.db')

# conectar a db
db.connect("../test_db.db")

# crear tablas
db.execute("""
    CREATE TABLE IF NOT EXISTS usuarios ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL, role TEXT DEFAULT 'cliente' )
""")

# has tables?
print(db.has_tables())
