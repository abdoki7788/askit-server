from sqlalchemy.orm import Session
from . import models, schemas
import datetime

def get_topic(db: Session, topic_id: int):
    return db.query(models.Topic).get(topic_id)

def get_topics(db: Session):
    return [{**i.__dict__, "answers_count": len(i.answers)} for i in list(db.query(models.Topic).all())]

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

def update_topic(db: Session, topic_id: int, topic_schema: schemas.TopicUpdate):
    topic = get_topic(db, topic_id)
    topic.title = topic_schema.title
    topic.content = topic_schema.content
    topic.updated_at = datetime.datetime.now()
    db.commit()
    return get_topic(db, topic_id)


# Answer crud functions
def get_answer(db: Session, answer_id: int):
    return db.query(models.Answer).get(answer_id)

def get_answers(db: Session, topic_id: int):
    return db.query(models.Topic).get(topic_id).answers

def create_answer(db: Session, answer: schemas.AnswerCreate, topic_id: int):
    db_answer = models.Answer(**answer.dict(), updated_at=datetime.datetime.now(), topic_id=topic_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer