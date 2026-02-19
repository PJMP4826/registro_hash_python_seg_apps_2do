from fastapi import APIRouter
from presentation.api.http.controllers.requests.create_user_request import CreateUserRequest
from presentation.api.http.controllers.create_user_controller import CreateUserController
from presentation.api.http.controllers.requests.change_password_request import ChangePasswordRequest
from presentation.api.http.controllers.change_password_controller import ChangePasswordController
from presentation.api.http.controllers.requests.change_role_request import ChangeRoleRequest
from presentation.api.http.controllers.change_role_controller import ChangeRoleController


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

@router.put("/cambiar-role")
async def change_password(request: ChangeRoleRequest):
    controller = ChangeRoleController()
    return await controller.handle(request)