from sqlalchemy.orm import Session
from tags import models

def get_tags(db: Session):
    return db.query(models.Tag).all()

def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).get(tag_id)

def get_tag_topics(db: Session, tag_id: int):
    return db.query(models.Tag).get(tag_id).topics