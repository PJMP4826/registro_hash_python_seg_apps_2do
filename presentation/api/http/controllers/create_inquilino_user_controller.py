from src.bootstrap.container import Container
from src.application.commands.create_user_with_inquilino_command import CreateInquilinoWithUserCommand
from fastapi import status
from fastapi.responses import JSONResponse
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError
from presentation.api.http.controllers.requests.create_user_with_inquilino_request import CreateInquilinoWithUserRequest


class CreateUserController:
    def __init__(self):
        self.container = Container()
        self.use_case = self.container.create_inquilino_with_user_use_case()

    async def handle(self, request_data: CreateInquilinoWithUserRequest):
        try:

            # Mapeo de los datos de la petición al DTO interno
            command = CreateInquilinoWithUserCommand(
                email=request_data.email,
                nombre_completo=request_data.nombre_completo,
                numero_departamento=request_data.numero_departamento,
                password=request_data.password,
                rol=request_data.rol,
                telefono=request_data.telefono,
            )

            self.use_case.execute(command=command)

            return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Usuario Registrado"}
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


