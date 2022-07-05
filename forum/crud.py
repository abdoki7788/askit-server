from sqlalchemy.orm import Session
from . import models, schemas
import datetime

def get_topic(db: Session, topic_id: int):
    return db.query(models.Topic).get(topic_id)

def get_topics(db: Session):
    return db.query(models.Topic).all()

def create_topic(db: Session, topic: schemas.TopicCreate):
    db_topic = models.Topic(**topic.dict(), updated_at=datetime.datetime.now())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def delete_topic(db: Session, topic_id: int):
    topic = get_topic(db, topic_id)
    db.delete(topic)
    db.commit()
    return topic

def voteup_topic(db: Session, topic_id: int):
    topic = get_topic(db, topic_id)
    topic.votes += 1
    db.commit()
    return topic.votes

def votedown_topic(db: Session, topic_id: int):
    topic = get_topic(db, topic_id)
    topic.votes -= 1
    db.commit()
    return topic.votes