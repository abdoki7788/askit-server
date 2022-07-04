from sqlalchemy.orm import Session
from . import models, schemas
import datetime

def get_topic(db: Session, topic_id: int):
    return db.query(models.Topic).filter(models.Topic.id == topic_id).first()

def get_topics(db: Session):
    return db.query(models.Topic).all()

def create_topic(db: Session, topic: schemas.TopicCreate):
    db_topic = models.Topic(**topic.dict(), updated_at=datetime.datetime.now())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic