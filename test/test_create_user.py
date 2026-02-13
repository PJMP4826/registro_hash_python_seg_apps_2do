from src.application.dto.create_user_dto import CreateUserDTO
from src.bootstrap.container import Container


# la data vendra de la request
#por ejemplo:
# input_dto = CreateUserDTO(
#     name=request.name,
#     email=request.email,
#     password=request.password,
# )

dto = CreateUserDTO(
    name="Fausto_Test",
    email="pato@outlook.com",
    password="Super_p@ssword_22",
    rol="admin"
)

container = Container()

use_case = container.create_user_use_case()

use_case.admin(dto=dto)

