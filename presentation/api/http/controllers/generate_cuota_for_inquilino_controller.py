from fastapi import status
from src.bootstrap.container import container
from fastapi.responses import JSONResponse
from src.application.commands.generate_cuota_for_command import (
    GenerateCuotaForInquilinoCommand,
)
from presentation.api.http.controllers.requests.generate_cuota_for_inquilino_request import (
    GenerateCuotaForInquilinoRequest,
)


class GenerateCuotaForInquilinoController:
    def __init__(self) -> None:
        self._use_case = container.generate_couta_for_inquilino_use_case()

    async def handle(self, request_data: GenerateCuotaForInquilinoRequest):
        try:

            # Mapeo de los datos de la petición al DTO interno
            command = GenerateCuotaForInquilinoCommand(
                dia_vencimiento=request_data.dia_vencimiento,
                email=request_data.email,
                month=request_data.month,
                year=request_data.year,
            )

            self._use_case.execute(command=command)

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "status": 200,
                    "message": "Cuota Registrada"
                },
            )

        except ValueError as e:
            # Captura de la validación de la contraseña
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"title": "Validation Error", "status": 400, "message": str(e)},
            )

        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "title": "Internal Server Error",
                    "status": 500,
                    "message": str(e),
                },
            )
