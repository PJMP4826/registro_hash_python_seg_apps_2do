class UserAlreadyExistsError(Exception):
    """Excepción cuando el correo electrónico ya está registrado"""
    def __init__(self, message: str):
        super().__init__(message) # Se pasa el mensaje a la clase padre