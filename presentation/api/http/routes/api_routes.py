from fastapi import APIRouter
from presentation.api.http.controllers.create_user_controller import CreateUserController
from src.application.dto.create_user_dto import CreateUserDTO

router = APIRouter()
controller = CreateUserController()

@router.post("/registro")
async def register_user(user_dto: CreateUserDTO):
    
    return await controller.handle(user_dto)