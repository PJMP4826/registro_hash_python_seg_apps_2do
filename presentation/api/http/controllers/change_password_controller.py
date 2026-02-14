from src.bootstrap.container import Container
from src.application.dto.change_password_dto import ChangePasswordDTO
from fastapi import status
from fastapi.responses import JSONResponse
from presentation.api.http.controllers.requests.change_password_request import ChangePasswordRequest

class ChangePasswordController:
    def __init__(self):
        self.container = Container()
        self.use_case = self.container.change_password_use_case()

    async def handle(self, request_data: ChangePasswordRequest):
        try:
            # Mapeo: Request (Web) al DTO (Aplicación)
            dto = ChangePasswordDTO(
                email=request_data.email,
                old_password_txt=request_data.old_password_txt,
                new_password_txt=request_data.new_password_txt
            )
            
            self.use_case.execute(dto)

            # Respuesta exitosa
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Contraseña actualizada exitosamente"}
            )

        except ValueError as e:
            # "Contraseña actual inválida" o "Usuario no existe"
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": str(e)}
            )
            
        except Exception as e:
            # Errores de base de datos o sistema
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": str(e)}
            )