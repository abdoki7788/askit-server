from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import schemas, crud
from db_config import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_decode_token(token, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = schemas.UserInDB(fake_decode_token(token))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user