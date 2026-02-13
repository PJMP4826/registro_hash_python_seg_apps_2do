from fastapi import APIRouter
from presentation.api.http.schemas import CreateUserRequest
from presentation.api.http.controllers.create_user_controller import CreateUserController

router = APIRouter()
controller = CreateUserController()

@router.post("/registro")
async def register_user(request: CreateUserRequest):
    # Pasamos el "request" directamente. El controlador se encarga del resto.
    return await controller.handle(request)