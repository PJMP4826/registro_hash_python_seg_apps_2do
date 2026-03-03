from fastapi import FastAPI, Depends
from presentation.api.http.routes import api_routes 
from presentation.api.http.routes import products_routes
from src.bootstrap.container import Container



# lifespan a la instancia de FastAPI
app = FastAPI(
    title="API de Usuarios",
    description="API construida con Arquitectura Limpia",
    version="1.0.0"
)

container = Container()

# middlewares
auth_middleware = container.get_json_middleware()

app.include_router(api_routes.router, prefix="/api/v1", tags=["Usuarios"])
app.include_router(products_routes.router, prefix="/api/v1", tags=["Productos"], dependencies=[Depends(auth_middleware.require_role("admin"))])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}