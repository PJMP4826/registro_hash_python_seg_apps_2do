from fastapi import APIRouter
from presentation.api.http.schemas import CreateUserRequest
from presentation.api.http.controllers.create_user_controller import CreateUserController


router = APIRouter()


@router.post("/registro")

async def register_user(request: CreateUserRequest):
    controller = CreateUserController()
    return await controller.handle(request)
