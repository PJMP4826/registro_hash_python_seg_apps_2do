from src.application.dto.change_rol_dto import ChangeRolDTO
from src.domain.value_objects.email import Email
from src.bootstrap.container import Container

container = Container()

change_rol_use_case = container.change_rol_use_case()

email = Email("faustojaviermendoza@gmail.com")

dto = ChangeRolDTO(
    email=email.value,
    password_txt="",
    rol="admin"
)

print(change_rol_use_case.execute(dto=dto))
