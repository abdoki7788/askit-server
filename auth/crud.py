from sqlalchemy.orm import Session
from auth import models, schemas, dependencies

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, hashed_password=dependencies.fake_hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user