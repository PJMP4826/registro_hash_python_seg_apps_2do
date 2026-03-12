from decimal import Decimal
from src.infrastructure.config.logger import logger
from src.domain.entities.departamento import Departamento
from src.domain.enums.departamento_status import DepartamentoStatus
from src.application.commands.create_departamento_command import (
    CreateDepartamentoCommand,
)
from src.infrastructure.repository.departamento_repository import DepartamentoRepository


class CreateDepartamento:
    def __init__(self, departamento_repository: DepartamentoRepository) -> None:
        self._repo = departamento_repository

    def execute(self, command: CreateDepartamentoCommand) -> bool:
        try:
            departamento_status = DepartamentoStatus(command.status)
        except ValueError as e:
            valid_status = ", ".join([estatus.value for estatus in DepartamentoStatus])
            logger.warning(f"El estatus {command.status} no es válido. estatus permitidos: {str(valid_status)}")
            raise ValueError(
                f"El estatus {command.status} no es válido. estatus permitidos: {str(valid_status)}"
            )

        try:
            departamento = Departamento.create(
                monto_renta=Decimal(command.monto_renta),
                num_departamento=command.num_departamento,
                piso=command.piso,
                status=departamento_status,
            )

            created = self._repo.create(departamento=departamento)

            if created and created > 0:
                return True

            return False
        except ValueError as ve:
            raise ve
        except Exception as e:
            logger.error(f"Error creando el departamento: {str(e)}")
            raise Exception(f"Error creando el departamento: {str(e)}")
