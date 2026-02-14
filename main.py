from contextlib import asynccontextmanager
from fastapi import FastAPI
from presentation.api.http.routes import api_routes 
from src.bootstrap.container import Container

# función que prepara la base de datos
def setup_database():
    try:
        # obtener conexión a la BD
        container = Container()
        db = container.db 
        
        query = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );
        """
        
        db.execute(query, ())
        print("Base de datos verificada: La tabla 'usuarios' está lista.")
        
    except Exception as e:
        print(f"Error al intentar crear la tabla automáticamente: {e}")

# ciclo de vida (Lifespan) de FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_database()
    
    yield
    
    print("Servidor apagado.")

# lifespan a la instancia de FastAPI
app = FastAPI(
    title="API de Usuarios",
    description="API construida con Arquitectura Limpia",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_routes.router, prefix="/api/v1", tags=["Usuarios"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}