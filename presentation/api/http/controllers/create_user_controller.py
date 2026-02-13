from src.bootstrap.container import Container
from src.application.dto.create_user_dto import CreateUserDTO
from fastapi import status
from fastapi.responses import JSONResponse
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError


class CreateUserController:
    def __init__(self):
        self.container = Container()
        self.use_case = self.container.create_user_use_case()

    async def handle(self, request_data):
        try:
        # Mapeo de los datos de la petición al DTO interno
            user_dto = CreateUserDTO(
                name=request_data.name,
                email=request_data.email,
                password=request_data.password,
                rol=request_data.rol
            )
            self.use_case.create_client_user(user_dto)

            return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Usuario Registrado"}
        )

        except ValueError:
            # Captura de la validación de la contraseña
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Credenciales Invalidas"}
            )

        except UserAlreadyExistsError as e:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": str(e)}  # Imprimirá: "El email X ya esta registrado"
            )
        
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": str(e)}
            )


