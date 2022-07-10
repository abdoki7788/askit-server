from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from auth import models, schemas, utils

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    try:
        db_user = models.User(username=user.username, hashed_password=utils.get_password_hash(user.password))
        db.add(db_user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(detail="User already exists", status_code=400)
    except ValueError as e:
        db.rollback()
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(detail="something wrong", status_code=500)
    db.refresh(db_user)
    return db_user