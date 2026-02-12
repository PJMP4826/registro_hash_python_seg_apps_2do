from connection_db import Database
from src.domain.entities import User

class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, user: User):
        try:
            
        except Exception as e:
            raise Exception()

    
        