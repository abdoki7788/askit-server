from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from auth import models, schemas, utils

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, id: str):
    return db.query(models.User).filter(models.User.id == id).first()

def get_users(db: Session):
    return db.query(models.User).all()

def update_user_me(db: Session, user, user_in: schemas.UserUpdate):
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    if user_in.about is not None:
        user.about = user_in.about
    db.commit()
    db.refresh(user)
    return user

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

def follow_user(db: Session, username: str, follower_username: str):
    db_user = get_user_by_username(db, username)
    db_follower = get_user_by_username(db, follower_username)
    if db_user is None:
        return None
    if db_follower not in db_user.followers:
        db_user.followers.append(db_follower)
    else:
        raise HTTPException(detail="User is already following", status_code=400)
    db.commit()
    db.refresh(db_user)
    return db_user.followers

def unfollow_user(db: Session, username: str, unfollower_username: str):
    db_user = get_user_by_username(db, username)
    db_unfollower = get_user_by_username(db, unfollower_username)
    if db_user is None:
        return None
    if db_unfollower in db_user.followers:
        db_user.followers.remove(db_unfollower)
    else:
        raise HTTPException(detail="User is not following", status_code=400)
    db.commit()
    db.refresh(db_user)
    return db_user.followers

def is_followed(db: Session, username: str, follower_username: str):
    db_user = get_user_by_username(db, username)
    db_follower = get_user_by_username(db, follower_username)
    if db_user is None:
        return None
    return db_follower in db_user.followers