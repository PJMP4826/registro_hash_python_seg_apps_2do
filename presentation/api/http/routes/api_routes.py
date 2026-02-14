from fastapi import APIRouter
from presentation.api.http.controllers.requests.create_user_request import CreateUserRequest
from presentation.api.http.controllers.create_user_controller import CreateUserController
from presentation.api.http.controllers.requests.change_password_request import ChangePasswordRequest
from presentation.api.http.controllers.change_password_controller import ChangePasswordController


router = APIRouter()


@router.post("/registro")

async def register_user(request: CreateUserRequest):
    controller = CreateUserController()
    return await controller.handle(request)

# Cambiar la contraseña
@router.put("/cambiar-password")
async def change_password(request: ChangePasswordRequest):
    controller = ChangePasswordController()
    return await controller.handle(request)