from src.application.use_cases.create_user import CreateUser
from src.application.dto.create_user_dto import CreateUserDTO
from src.application.commands.create_inquilino_command import CreateInquilinoCommand
from src.application.commands.create_user_with_inquilino_command import (
    CreateInquilinoWithUserCommand,
)
from src.application.use_cases.crear_inquilino_and_assign_departamento import (
    CreateInquilinoAndAssignDepartamento,
)
from src.infrastructure.config.logger import logger


class CreateInquilinoWithUser:
    def __init__(
        self,
        create_user_use_case: CreateUser,
        create_inquilino_assign_departamento_use_case: CreateInquilinoAndAssignDepartamento,
    ) -> None:
        self._create_user_use_case = create_user_use_case
        self._create_inquilino_assign_departamento_use_case = (
            create_inquilino_assign_departamento_use_case
        )

    def execute(self, command: CreateInquilinoWithUserCommand) -> bool:
        inquilino_command = CreateInquilinoCommand(
            nombre_completo=command.nombre_completo,
            numero_departamento=command.numero_departamento,
            telefono=command.telefono,
        )

        user_dto = CreateUserDTO(
            email=command.email,
            name=command.nombre_completo,
            password=command.password,
            rol=command.rol,
        )

        inquilino_id = self._create_inquilino_assign_departamento_use_case.execute(
            command=inquilino_command
        )

        self._create_user_use_case.create_client_user(
            dto=user_dto, inquilino_id=inquilino_id
        )

        logger.debug(
            f"Usuario {user_dto.name} vinculado con inquilino {inquilino_command.nombre_completo}"
        )
        
        return True
