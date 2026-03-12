from src.application.commands.create_inquilino_command import CreateInquilinoCommand
from src.domain.entities.inquilino import Inquilino
from src.infrastructure.repository.inquilino_repository import InquilinoRepository
from src.infrastructure.repository.departamento_repository import DepartamentoRepository
from src.infrastructure.config.logger import logger

class CreateInquilinoAndAssignDepartamento:
    def __init__(
        self,
        inquilino_repo: InquilinoRepository,
        departamento_repo: DepartamentoRepository,
    ):
        self._inquilino_repo = inquilino_repo
        self._departamento_repo = departamento_repo

    def execute(self, command: CreateInquilinoCommand) -> int | None:

        # verificar que el departamento exista y este disponible
        departamento = self._departamento_repo.get_by_numero_departamento(command.numero_departamento)

        if not departamento:
            logger.warning("El departamento no existe")
            raise ValueError("El departamento no existe")

        if not departamento.is_available():
            logger.warning("El departamento ya esta ocupado")
            raise ValueError("El departamento ya esta ocupado")

        inquilino = Inquilino(
            id=0,  # se ignora, lo asigna la BD
            nombre_completo=command.nombre_completo,
            telefono=command.telefono,
            departamento_id=departamento.id,
        )

        nuevo_id = self._inquilino_repo.create(inquilino)

        logger.info(f"Inquilino {command.nombre_completo} alojado en el departamento numero {departamento.num_departamento}")

        # marcar departamento como ocupado
        departamento.mark_as_occupied()

        logger.info(f"Departamento numero {departamento.num_departamento} cambio a {departamento.status.value}")

        self._departamento_repo.update_status(
            id_=departamento.id, status=departamento.status
        )

        return nuevo_id
