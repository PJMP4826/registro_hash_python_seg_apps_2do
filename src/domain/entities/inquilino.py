class Inquilino:
    def __init__(
        self,
        id: int,
        nombre_completo: str,
        telefono: str,
        departamento_id: int,
        estatus: bool = True,
    ):
        self.id = id
        self.nombre_completo = nombre_completo
        self.telefono = telefono
        self.departamento_id = departamento_id
        self.estatus = estatus

    def deactivate(self):
        self.estatus = False

    def activate(self):
        self.estatus = True

    def is_active(self):
        return self.estatus
