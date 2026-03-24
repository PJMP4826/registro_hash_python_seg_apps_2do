from fastapi import FastAPI, Depends
from presentation.api.http.routes import general_routes
from presentation.api.http.routes import client_routes 
from presentation.api.http.routes import admin_routes
from src.bootstrap.container import Container
from presentation.middleware.cors_middleware import add_cors_middleware



app = FastAPI(
    title="API de Usuarios",
    description="API construida con Arquitectura Limpia",
    version="1.0.0"
)

add_cors_middleware(app=app)

container = Container()

# middlewares
auth_middleware = container.get_json_middleware()

app.include_router(general_routes.router, prefix="/api/v1", tags=["Usuarios"])
app.include_router(
    client_routes.router, 
    prefix="/api/v1", tags=["Clientes"], 
    dependencies=[Depends(auth_middleware.require_role("cliente"))]
    )
app.include_router(
    admin_routes.router, 
    prefix="/api/v1", tags=["Admin"], 
    dependencies=[Depends(auth_middleware.require_role("admin"))]
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}