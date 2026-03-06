from fastapi import APIRouter
from presentation.api.http.controllers.authenticate_user_controller import (
    AuthenticateUserController,
)
from presentation.api.http.controllers.requests.authenticate_user_request import (
    AuthenticateUserRequest,
)


router = APIRouter()


@router.post("/login")
async def login(request: AuthenticateUserRequest):
    controller = AuthenticateUserController()
    return await controller.handle(request)
