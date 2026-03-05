from src.bootstrap.container import container
from src.application.commands.create_inquilino_command import CreateInquilinoCommand

command = CreateInquilinoCommand(
    nombre_completo="User Test",
    numero_departamento=3,
    telefono="NNNNNNNN"
)

use_case = container.crear_inquilino_and_assign_departamento_use_case()

print("Inquilino id: ", use_case.execute(command=command))

