from fastapi import FastAPI

from presentation.api.http.routes import api_routes 

app = FastAPI(
    title="API de Usuarios",
    description="API construida con Arquitectura Limpia",
    version="1.0.0"
)

app.include_router(api_routes.router, prefix="/api/v1", tags=["Usuarios"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}