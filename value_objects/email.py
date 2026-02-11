class Email:
    def __init__(self, email: str):
        self.value: str = email

        if not "@" in self.value:
            return ValueError("Email invalido") 
    