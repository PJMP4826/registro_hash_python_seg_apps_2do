from src.bootstrap.container import Container

class CreateUserController:
    def __init__(self):
        self.container = Container()
        self.use_case = self.container.create_user_use_case()