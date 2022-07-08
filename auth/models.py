from db_config import Base, engine
from sqlalchemy import Column, Integer, String, Boolean
from . import models

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)