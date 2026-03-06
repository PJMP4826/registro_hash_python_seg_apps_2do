from fastapi import APIRouter
from presentation.api.http.controllers.requests.create_user_with_inquilino_request import CreateInquilinoWithUserRequest
from presentation.api.http.controllers.create_inquilino_user_controller import (
    CreateUserController,
)
from presentation.api.http.controllers.requests.change_password_request import (
    ChangePasswordRequest,
)
from presentation.api.http.controllers.change_password_controller import (
    ChangePasswordController,
)
from presentation.api.http.controllers.requests.change_role_request import (
    ChangeRoleRequest,
)
from presentation.api.http.controllers.change_role_controller import (
    ChangeRoleController,
)
from presentation.api.http.controllers.authenticate_user_controller import (
    AuthenticateUserController,
)
from presentation.api.http.controllers.requests.authenticate_user_request import (
    AuthenticateUserRequest,
)

from presentation.api.http.controllers.create_departamento_controller import (
    CreateDepartamentoController,
)

from presentation.api.http.controllers.requests.create_departamento_request import (
    CreateDepartamentoRequest
)

from presentation.api.http.controllers.generate_cuota_for_inquilino_controller import (
    GenerateCuotaForInquilinoController
)

from presentation.api.http.controllers.requests.generate_cuota_for_inquilino_request import (
    GenerateCuotaForInquilinoRequest
)


router = APIRouter()


@router.post("/registro-clientes")
async def register_user(request: CreateInquilinoWithUserRequest):
    controller = CreateUserController()
    return await controller.handle(request)


# Cambiar la contraseña
@router.put("/cambiar-password")
async def change_password(request: ChangePasswordRequest):
    controller = ChangePasswordController()
    return await controller.handle(request)


@router.put("/cambiar-role")
async def change_role(request: ChangeRoleRequest):
    controller = ChangeRoleController()
    return await controller.handle(request)


@router.post("/login")
async def login(request: AuthenticateUserRequest):
    controller = AuthenticateUserController()
    return await controller.handle(request)

@router.post("/crear-departamento")
async def create_departamento(request: CreateDepartamentoRequest):
    controller = CreateDepartamentoController()
    return await controller.handle(request)

@router.post("/generate-couta")
async def generate_cuota(request: GenerateCuotaForInquilinoRequest):
    controller = GenerateCuotaForInquilinoController()
    return await controller.handle(request)
