from fastapi import APIRouter
from presentation.api.http.controllers.create_user_controller import CreateUserController
from presentation.api.http.controllers.requests.create_user_request import CreateUserRequest

router = APIRouter()
controller = CreateUserController()

@router.post("/registro")
async def register_user(user_dto: CreateUserRequest):
    
    return await controller.handle(user_dto)