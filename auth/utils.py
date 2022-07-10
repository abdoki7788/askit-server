import re
from typing import Union
from jose import jwt
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from passlib.context import CryptContext
from auth import crud
import settings
from db_config import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if re.fullmatch(regex, password):
        return pwd_context.hash(password)
    else:
        raise ValueError('Password must be at least 6 characters long and contain at least one number, one uppercase letter, one lowercase letter, one special character and one of the following: @#$%^&-+=()')

def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_user_by_username(db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)
    return encoded_jwt