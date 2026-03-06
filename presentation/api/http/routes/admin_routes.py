from fastapi import APIRouter
from presentation.api.http.controllers.requests.create_user_with_inquilino_request import CreateInquilinoWithUserRequest
from presentation.api.http.controllers.create_inquilino_user_controller import (
    CreateUserController,
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

@router.post("/crear-departamento")
async def create_departamento(request: CreateDepartamentoRequest):
    controller = CreateDepartamentoController()
    return await controller.handle(request)

@router.post("/generate-couta")
async def generate_cuota(request: GenerateCuotaForInquilinoRequest):
    controller = GenerateCuotaForInquilinoController()
    return await controller.handle(request)