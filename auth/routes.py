from typing import List
from fastapi.routing import APIRouter
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from auth import schemas, crud, dependencies, utils
from db_config import get_db
import settings

routes = APIRouter(prefix="/auth", tags=["auth"])

@routes.put("/users/me", response_model=schemas.UserMe)
async def update_users_me(body: schemas.UserUpdate, current_user: schemas.UserCreate = Depends(dependencies.get_current_user), db: Session = Depends(get_db)):
    try:
        return crud.update_user_me(db=db, user=current_user, user_in=body)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@routes.get("/users/me", response_model=schemas.UserMe)
async def get_users_me(current_user: schemas.UserCreate = Depends(dependencies.get_current_user)):
    return current_user

@routes.get("/users", response_model=List[schemas.UserProfile])
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@routes.get("/users/{username}", response_model=schemas.UserProfile)
async def get_user(username: str, db: Session = Depends(get_db)):
    data = crud.get_user_by_username(db, username)
    if data is not None:
        return data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@routes.patch("/users/{username}/follow", response_model=List[schemas.UserResponse])
async def follow_user(username: str, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(dependencies.get_current_user)):
    data = crud.follow_user(db, username, current_user.username)
    if data is not None:
        return data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@routes.patch("/users/{username}/unfollow", response_model=List[schemas.UserResponse])
async def unfollow_user(username: str, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(dependencies.get_current_user)):
    data = crud.unfollow_user(db, username, current_user.username)
    if data is not None:
        return data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@routes.get("/users/{username}/isfollowed")
async def is_followed(username: str, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(dependencies.get_current_user)):
    data = crud.is_followed(db, username, current_user.username)
    if data is not None:
        return data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

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
    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = utils.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
