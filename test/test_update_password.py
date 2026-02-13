from src.application.dto.change_password_dto import ChangePasswordDTO
from src.domain.value_objects.email import Email
from src.bootstrap.container import Container

container = Container()

change_password_use_case = container.change_password_use_case()

email = Email("pato@outlook.com")

dto = ChangePasswordDTO(
    email=email.value,
    old_password_txt="Qmd.15M12&",
    new_password_txt="P@ssword_2"
)

print(change_password_use_case.execute(dto=dto))
