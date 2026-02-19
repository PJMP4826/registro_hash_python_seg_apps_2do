from src.bootstrap.container import Container
from src.application.dto.change_rol_dto import ChangeRolDTO
from fastapi import status
from fastapi.responses import JSONResponse
from presentation.api.http.controllers.requests.change_role_request import ChangeRoleRequest 

class ChangeRoleController:
    def __init__(self):
        self.container = Container()
        self.use_case = self.container.change_rol_use_case()

    async def handle(self, request_data: ChangeRoleRequest):
        try:
            # Mapeo: Request (Web) al DTO (Aplicacion)
            dto = ChangeRolDTO(
                email=request_data.email,
                password_txt=request_data.password_txt,
                rol=request_data.role
            )
            
            self.use_case.execute(dto)

            # Respuesta exitosa
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Role actualizado exitosamente"}
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
