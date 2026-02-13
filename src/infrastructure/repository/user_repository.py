from src.domain.value_objects.email import Email
from src.infrastructure.config.database import Database
from src.domain.entities.user import User


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def email_exists(self, email: Email) -> bool:
        query = "SELECT COUNT(*) as count FROM usuarios WHERE email = ?"
        result = self.db.execute_query_fetchone(query, (str(email),))
        print("Cantidad de emails: ", result)
        return result[0] > 0

    def create_user(self, user: User) -> bool:
        try:
            if self.email_exists(user.email):
                raise ValueError(f"El email {user.email.value} ya esta registrado")

            query = """
                    INSERT INTO usuarios (name, email, password, role)
                    VALUES (?, ?, ?, ?)
                    """

            self.db.execute(query, (
                str(user.name),
                str(user.email.value),
                user.password.hashed_value,
                user.role.value
            ))

            return True
        except Exception as e:
            raise Exception("Error al crear el usuario")
