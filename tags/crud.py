from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from tags import models

def create_tag(db: Session, tag: str):
    try:
        tag = models.Tag(**tag.dict())
        db.add(tag)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Tag already exists")
    return tag

def get_tags(db: Session):
    return db.query(models.Tag).all()

def get_or_create_tag(db: Session, name: int):
    tag = db.query(models.Tag).filter(models.Tag.name == name).first()
    if tag is None:
        tag = models.Tag(name=name)
        db.add(tag)
        db.commit()
    return tag

def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).get(tag_id)

def get_tag_topics(db: Session, tag_id: int):
    return get_tag(db=db, tag_id=tag_id).topics