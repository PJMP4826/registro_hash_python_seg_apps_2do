from fastapi import status
from src.bootstrap.container import Container
from fastapi.responses import JSONResponse
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError
from src.application.commands.create_user_admin_command import CreateUserAdminCommand
from presentation.api.http.controllers.requests.create_user_admin_request import CreateUserAdminRequest


class CreateUserAdminController:
    def __init__(self):
        self.container = Container()
        self._use_case = self.container.create_user_use_case()

    async def handle(self, request_data: CreateUserAdminRequest):
        try:

            command = CreateUserAdminCommand(
                email=request_data.email,
                name=request_data.name,
                password=request_data.password
            )

            self._use_case.create_admin_user(command=command)

            return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": 201,
                "message": "Usuario Administrador Registrado"
            }
        )

        except ValueError as e:
            # Captura de la validación de la contraseña
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "title": "Validation Error",
                    "status": 400,
                    "message": str(e)
                }
            )


        except UserAlreadyExistsError as e:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "title": "User already exists error",
                    "status": 409,
                    "message": str(e)
                }
                # Imprimirá: "El email X ya esta registrado"
            )
        
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "title": "Internal Server Error",
                    "status": 500,
                    "message": str(e)
                }
            )


