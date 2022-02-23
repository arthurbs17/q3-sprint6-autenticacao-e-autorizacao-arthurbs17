from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Column, String, Integer

from app.configs.database import db


@dataclass
class User(db.Model):
    name: str
    last_name: str
    email: str

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False)
    last_name = Column(String(511), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(511), nullable=False)
    api_key = Column(String(511), nullable=False)


    @property
    def password(self):
        return AttributeError("Password is not accessible!")


    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    
    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)