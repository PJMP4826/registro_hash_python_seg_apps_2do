from src.bootstrap.container import Container
from fastapi import status
from fastapi.responses import JSONResponse
from src.application.dto.authenticate_user_dto import AuthenticateUserDTO
from presentation.api.http.controllers.requests.authenticate_user_request import AuthenticateUserRequest 

class AuthenticateUserController:
    def __init__(self):
        self.container = Container()
        self.use_case = self.container.login_use_case()

    async def handle(self, request_data: AuthenticateUserRequest):
        try:
            # Mapeo: Request (Web) al DTO (Aplicacion)
            dto = AuthenticateUserDTO(
                email=request_data.email,
                password_txt=request_data.password_txt,
            )
            
            self.use_case.execute(dto)

            # Respuesta exitosa
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Credenciales Correctas :)"}
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

            
        except Exception as e:
            # Errores de base de datos o sistema
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "title": "Internal Server Error",
                    "status": 500,
                    "message": str(e)
                }
            )
