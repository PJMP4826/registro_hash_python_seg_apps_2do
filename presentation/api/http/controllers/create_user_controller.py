from src.bootstrap.container import Container
from src.application.dto.create_user_dto import CreateUserDTO


class CreateUserController:
    def __init__(self):
        self.container = Container()
        self.use_case = self.container.create_user_use_case()

    async def handle(self, request_data):
        
        # Mapeo de los datos de la petición al DTO interno
        user_dto = CreateUserDTO(
            name=request_data.name,
            email=request_data.email,
            password=request_data.password,
            rol=request_data.rol
        )
        return self.use_case.create_client_user(user_dto)