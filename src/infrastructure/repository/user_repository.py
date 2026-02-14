from src.domain.exceptions.user_exceptions import UserAlreadyExistsError
from src.domain.value_objects.email import Email
from src.infrastructure.config.database import Database
from src.domain.entities.user import User


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def email_exists(self, email: Email) -> bool:
        query = "SELECT COUNT(*) as count FROM usuarios WHERE email = ?"
        result = self.db.execute_query_fetchone(query, (str(email.value),))
        print("Cantidad de emails: ", result)
        return result[0] > 0

    def create_user(self, user: User) -> bool:
        if self.email_exists(user.email):
            # pasar el mensaje a la nueva excepción
            raise UserAlreadyExistsError(f"El email {user.email.value} ya esta registrado")

        try:
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
            raise Exception(f"Error al crear el usuario: {str(e)}")

    def get_password_hash_by_email(self, email: Email):
        try:
            if not self.email_exists(email=email):
                raise ValueError(f"El email {email.value} no se encuentra registrado")

            query = "SELECT password FROM usuarios WHERE email = ?"

            result = self.db.execute_query_fetchone(query, (str(email.value), ))
            if result:
                return result[0]

            return None
        
        except ValueError as ve:
            raise ve
        except Exception as e:

            raise Exception(f"Error al obtener el hash de la contraseña: {str(e)}")

    def update_password(self, password_hash: str, email: Email) -> bool:
        try:
            query = """
                UPDATE usuarios SET password = ? WHERE email = ?
            """

            self.db.execute(query, (
                password_hash,
                email.value
            ))

            return True
        except Exception as e:
            raise Exception(f"Error al actualizar la contraseña: {str(e)}")
