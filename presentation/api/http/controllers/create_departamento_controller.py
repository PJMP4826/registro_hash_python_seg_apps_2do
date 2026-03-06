from fastapi import status
from src.bootstrap.container import container
from fastapi.responses import JSONResponse
from src.application.commands.create_departamento_command import CreateDepartamentoCommand
from presentation.api.http.controllers.requests.create_departamento_request import CreateDepartamentoRequest

class CreateDepartamentoController:
    def __init__(self) -> None:
        self._use_case = container.create_departamento_use_case()

    async def handle(self, request_data: CreateDepartamentoRequest):
        try:
            # Mapeo: Request (Web) al DTO (Aplicacion)
            command = CreateDepartamentoCommand(
                monto_renta=request_data.monto_renta,
                num_departamento=request_data.num_departamento,
                piso=request_data.piso,
                status=request_data.status
            )
            
            self._use_case.execute(command=command)

            # Respuesta exitosa
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Departamento creado exitosamente exitosamente"}
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

            