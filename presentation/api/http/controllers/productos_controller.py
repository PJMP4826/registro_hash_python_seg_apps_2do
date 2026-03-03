from fastapi import status
from fastapi.responses import JSONResponse

_productos_db: dict[str, dict] = {
    "1": {"id": "1", "nombre": "Laptop", "precio": 999.99, "stock": 10},
    "2": {"id": "2", "nombre": "Mouse", "precio": 29.99, "stock": 50},
    "3": {"id": "3", "nombre": "Teclado", "precio": 49.99, "stock": 30},
}


class ProductosController:
    def __init__(self):
        self._db = _productos_db

    async def get_all(self):
        try:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"productos": list(self._db.values())},
            )

        except ValueError as e:
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
