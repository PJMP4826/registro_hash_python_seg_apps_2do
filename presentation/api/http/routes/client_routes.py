from fastapi import APIRouter
from presentation.api.http.controllers.requests.change_password_request import (
    ChangePasswordRequest,
)
from presentation.api.http.controllers.change_password_controller import (
    ChangePasswordController,
)

router = APIRouter()


# Cambiar la contraseña
@router.put("/cambiar-password-cliente")
async def change_password(request: ChangePasswordRequest):
    controller = ChangePasswordController()
    return await controller.handle(request)


# @router.put("/cambiar-role")
# async def change_role(request: ChangeRoleRequest):
#     controller = ChangeRoleController()
#     return await controller.handle(request)
