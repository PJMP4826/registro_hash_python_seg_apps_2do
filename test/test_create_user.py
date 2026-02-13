from src.domain.entities.user import User
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.infrastructure.config.database import Database

from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher

from src.infrastructure.repository.user_repository import UserRepository
from src.domain.enums.user_role import UserRole

hasher = BcryptPasswordHasher()

user_password = Password.create_from_text("12222gdfdgdM@", hasher)

user = User(
    name='Fausto',
    email=Email("fausto@gmail.com"),
    password=user_password,
    password_hasher=hasher,
    role=UserRole.CLIENTE
)

db = Database()
db.connect("../test_db.db")

repo = UserRepository(db=db)
repo.create_user(user=user)

print(user)

# hash de la password
print(user.password.hashed_value)
