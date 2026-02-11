class Password:
     def __init__(self, password: str):
        self.value = password

        if len(self.value) < 8:
            return ValueError("La contraseña debe ser mayor a 8 caracteres")

        if len(self.value) > 10:
            return ValueError("La contraseña debe ser menor a 10 caracteres")