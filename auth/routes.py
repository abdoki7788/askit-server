from typing import List
from fastapi.routing import APIRouter
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from auth import schemas, crud, dependencies
from db_config import get_db

routes = APIRouter()

@routes.get("/users/me")
async def read_users_me(current_user: schemas.UserCreate = Depends(get_current_user)):
    return current_user

@routes.get('/users', response_model=List[schemas.UserResponse])
async def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@routes.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@routes.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_dict = crud.get_user_by_username(db, form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = schemas.UserInDB(**user_dict.__dict__)
    hashed_password = dependencies.fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "Bearer"}
