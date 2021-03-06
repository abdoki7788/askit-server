from fastapi import HTTPException
from slugify import slugify
from sqlalchemy.orm import Session
from . import models, schemas
from auth import crud as auth_crud
from tags.crud import get_or_create_tag
import datetime

def get_topic(db: Session, topic_id: int):
    data = db.query(models.Topic).get(topic_id)
    if data is not None:
        return data
    else:
        raise HTTPException(status_code=404, detail="Topic not found")

def get_topic_by_slug(db: Session, slug: str):
    return db.query(models.Topic).filter(models.Topic.slug == slug).first()

def get_topics(db: Session):
    return db.query(models.Topic).all()

def get_hot_topics(db: Session):
    return db.query(models.Topic).filter(models.Topic.created_at > datetime.datetime.now() - datetime.timedelta(days=7)).order_by(models.Topic.votes_count.desc()).limit(10).all()

def create_topic(db: Session, topic: schemas.TopicCreate, user_id: int):
    data = topic.dict()
    data["tags"] = [get_or_create_tag(db, i) for i in topic.tags]
    if get_topic_by_slug(db, slugify(data["title"])):
        raise HTTPException(status_code=400, detail="Topic with this title already exists")
    db_topic = models.Topic(**data, updated_at=datetime.datetime.now(), creator_id=user_id, slug=slugify(data["title"]))
    auth_crud.get_user_by_id(db, user_id).score += 30
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def delete_topic(db: Session, topic_id: int):
    topic = get_topic(db, topic_id)
    db.delete(topic)
    db.commit()
    return topic

def voteup_topic(db: Session, topic_id: int, user):
    topic = get_topic(db, topic_id)
    if topic.creator_id != user.id and user not in topic.votes:
        topic.votes.append(user)
        topic.votes_count += 1
        topic.creator.score += 10
    elif user.id == topic.creator_id:
        raise HTTPException(status_code=403, detail="You can not voteup yourself")
    elif user in topic.votes:
        raise HTTPException(status_code=400, detail="User has already voted for this topic")
    db.commit()
    print(topic.votes)
    return topic.votes

def votedown_topic(db: Session, topic_id: int, user):
    topic = get_topic(db, topic_id)
    if user in topic.votes and user.id != topic.creator_id:
        topic.votes.remove(user)
        topic.votes_count -= 1
        topic.creator.score -= 10
    elif user not in topic.votes:
        raise HTTPException(status_code=400, detail="User has not voted for this topic")
    elif user.id == topic.creator_id:
        raise HTTPException(status_code=403, detail="You can not votedown yourself")
    db.commit()
    return topic.votes

def update_topic(db: Session, topic_id: int, topic_schema: schemas.TopicUpdate):
    topic = get_topic(db, topic_id)
    topic.title = topic_schema.title
    topic.content = topic_schema.content
    topic.updated_at = datetime.datetime.now()
    db.commit()
    return get_topic(db, topic_id)

def add_favorite_topic(db: Session, topic_id: int, user):
    topic = get_topic(db, topic_id)
    if topic not in user.favorites:
        user.favorites.append(topic)
    else:
        raise HTTPException(status_code=400, detail="User has already favorited this topic")
    db.commit()
    return user.favorites

def remove_favorite_topic(db: Session, topic_id: int, user):
    topic = get_topic(db, topic_id)
    if topic in user.favorites:
        user.favorites.remove(topic)
    else:
        raise HTTPException(status_code=400, detail="User has not favorited this topic")
    db.commit()
    return user.favorites

def is_favorite_topic(db: Session, topic_id: int, user):
    topic = get_topic(db, topic_id)
    return topic in user.favorites

# Answer crud functions
def get_answer(db: Session, answer_id: int):
    return db.query(models.Answer).get(answer_id)

def get_answers(db: Session, topic_id: int):
    return db.query(models.Topic).get(topic_id).answers

def create_answer(db: Session, answer: schemas.AnswerCreate, topic_id: int, creator_id: int):
    db_answer = models.Answer(**answer.dict(), updated_at=datetime.datetime.now(), topic_id=topic_id, creator_id=creator_id)
    db.add(db_answer)
    auth_crud.get_user_by_id(db, creator_id).score += 50
    db.commit()
    db.refresh(db_answer)
    return db_answer

def voteup_answer(db: Session, answer_id: int, user):
    answer = get_answer(db, answer_id)
    if answer.creator_id != user.id and user not in answer.votes:
        answer.votes.append(user)
        answer.votes_count += 1
        answer.creator.score += 10
    elif user.id == answer.creator_id:
        raise HTTPException(status_code=403, detail="You can not voteup yourself")
    elif user in answer.votes:
        raise HTTPException(status_code=400, detail="User has already voted for this answer")
    db.commit()
    return answer.votes

def votedown_answer(db: Session, answer_id: int, user):
    answer = get_answer(db, answer_id)
    if user in answer.votes and user.id != answer.creator_id:
        answer.votes.remove(user)
        answer.votes_count -= 1
        answer.creator.score -= 10
    elif user not in answer.votes:
        raise HTTPException(status_code=400, detail="User has not voted for this answer")
    elif user.id == answer.creator_id:
        raise HTTPException(status_code=403, detail="You can not votedown yourself")
    db.commit()
    return answer.votes