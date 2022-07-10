from typing import List
from fastapi.routing import APIRouter
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from auth import schemas, crud, dependencies, utils
from db_config import get_db
import settings

routes = APIRouter(prefix="/auth")

@routes.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: schemas.UserCreate = Depends(dependencies.get_current_user)):
    return current_user

@routes.get("/users", response_model=List[schemas.UserResponse])
async def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@routes.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@routes.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = utils.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
