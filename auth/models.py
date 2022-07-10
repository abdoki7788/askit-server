from db_config import Base
import re
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)

    @validates('username')
    def validate_username(self, key, username):
        if re.fullmatch(r"^[a-z0-9_-]{3,15}$", username) is None:
            raise ValueError('Username must be at least 3 characters long and contain only letters, numbers, underscores, and dashes.')
        return username
    
    @validates('full_name')
    def validate_full_name(self, key, full_name):
        if re.fullmatch(r"^[a-zA-Z ]{3,30}$", full_name) is None:
            raise ValueError('Full name must be at least 3 characters long and contain only letters.')
        return full_name
    
    @validates('email')
    def validate_email(self, key, email):
        if re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is None:
            raise ValueError('Email must be a valid email address.')
        return email