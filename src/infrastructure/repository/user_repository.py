from src.domain.entities.user import User
from src.domain.value_objects.email import Email
from src.infrastructure.config.logger import logger
from src.infrastructure.config.database import Database
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def email_exists(self, email: str) -> bool:
        query = "SELECT COUNT(*) as count FROM usuarios WHERE email = ?"
        result = self.db.execute_query_fetchone(query, (str(email),))
        # print("Cantidad de emails: ", result)
        return result[0] > 0 # type: ignore

    def create_user(self, user: User) -> bool:
        if self.email_exists(user.email.value):
            # pasar el mensaje a la nueva excepción
            logger.warning(f"El email {user.email.value} ya esta registrado")
            raise UserAlreadyExistsError(
                f"El email {user.email.value} ya esta registrado"
            )

        try:
            query = """
                    INSERT INTO usuarios (uuid, name, email, password, role, inquilino_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """

            self.db.execute(
                query,
                (
                    str(user.uuid),
                    str(user.name),
                    str(user.email.value),
                    user.password.hashed_value,
                    user.role.value,
                    user.inquilino_id # puede ser null cuando se crea un usuario admin (el admin no es inquilino)
                ),
            )

            return True
        except Exception as e:
            logger.error(f"Error al crear el usuario: {str(e)}")
            raise Exception(f"Error al crear el usuario")

    def get_user_by_email(self, email: str) -> User | None:
        if not self.email_exists(email=email):
            logger.warning(f"El email {email} no se encuentra registrado")
            raise ValueError(f"El email {email} no se encuentra registrado")

        try:
            query = "SELECT uuid, name, email, password, role, inquilino_id FROM usuarios WHERE email = ?"

            result = self.db.execute_query_fetchone(query, (str(email),))

            if result:
                return User.from_dict({
                    "uuid": result[0],
                    "name": result[1],
                    "email": result[2],
                    "password": result[3],
                    "role": result[4],
                    "inquilino_id": result[5]
                })

            return None
        except Exception as e:
            logger.error(f"Error al consultar los datos del usuario: {str(e)}")
            raise Exception(f"Error al consultar los datos del usuario")

    def get_password_hash_by_email(self, email: str):
        try:
            if not self.email_exists(email=email):
                logger.warning(f"El email {email} no se encuentra registrado")
                raise ValueError(f"El email {email} no se encuentra registrado")

            query = "SELECT password FROM usuarios WHERE email = ?"

            result = self.db.execute_query_fetchone(query, (str(email),))
            if result:
                return result[0]

            return None

        except ValueError as ve:
            raise ve
        except Exception as e:
            logger.error(f"Error al obtener el hash de la contraseña: {str(e)}")
            raise Exception(f"Error al obtener el hash de la contraseña")

    def update_password(self, password_hash: str, email: Email) -> bool:
        try:
            query = """
                UPDATE usuarios SET password = ? WHERE email = ?
            """

            self.db.execute(query, (password_hash, email.value))

            return True
        except Exception as e:
            logger.error(f"Error al actualizar la contraseña: {str(e)}")
            raise Exception(f"Error al actualizar la contraseña")

    def update_rol(self, rol_type: str, email: str) -> bool:
        try:
            if not self.email_exists(email=email):
                logger.warning(f"El email {email} no se encuentra registrado")
                raise ValueError(f"El email {email} no se encuentra registrado")

            query = """
                UPDATE usuarios SET role = ? WHERE email = ?
            """

            self.db.execute(query, (rol_type, email))

            return True
        except ValueError as ve:
            raise ve

        except Exception as e:
            logger.error(f"Error al actualizar el rol: {str(e)}")
            raise Exception("Error al actualizar el rol")
