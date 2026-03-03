from fastapi import APIRouter
from presentation.api.http.controllers.productos_controller import ProductosController

router = APIRouter()


@router.get("/products")
async def get_products():
    controller = ProductosController()
    return await controller.get_all()
