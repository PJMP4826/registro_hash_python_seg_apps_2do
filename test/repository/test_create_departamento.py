from decimal import Decimal
from src.bootstrap.container import container
from src.domain.entities.departamento import Departamento

repo = container.departamento_repository

dep = Departamento(
    id=0,
    num_departamento=3,
    monto_renta=Decimal("1000"),
    piso=2,
)

print(repo.create(departamento=dep))


