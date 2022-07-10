from fastapi import APIRouter, Body, Depends
from typing import List
from sqlalchemy.orm import Session
from jose import jwt
from . import crud, schemas
from auth.dependencies import oauth2_scheme
from db_config import get_db
import settings

routes = APIRouter(prefix="/topics")

@routes.post("", response_model=schemas.TopicResponse, status_code=201)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])["sub"]
    return crud.create_topic(db=db, topic=topic, user_id=user_id)

@routes.get("", response_model=List[schemas.TopicListResponse], status_code=200)
def topics(db: Session = Depends(get_db)):
    return crud.get_topics(db=db)

@routes.get("/{topic_id}", response_model=schemas.TopicResponse, status_code=200)
def topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.get_topic(db=db, topic_id=topic_id)

@routes.delete("/{topic_id}", status_code=204)
def delete_topic(topic_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.delete_topic(db=db, topic_id=topic_id)

@routes.put("/{topic_id}", status_code=200)
def update_topic(topic_id: int, db: Session = Depends(get_db), topic: schemas.TopicUpdate = Body(), token: str = Depends(oauth2_scheme)):
    return crud.update_topic(db=db, topic_id=topic_id, topic_schema=topic)

@routes.patch("/{topic_id}/voteup", status_code=200)
def voteup_topic(topic_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.voteup_topic(db=db, topic_id=topic_id)

@routes.patch("/{topic_id}/votedown", status_code=200)
def votedown_topic(topic_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.votedown_topic(db=db, topic_id=topic_id)

@routes.post("/{topic_id}/answers", response_model=schemas.AnswerResponse, status_code=201)
def create_answer(topic_id: int, answer: schemas.AnswerCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.create_answer(db=db, answer=answer, topic_id=topic_id)

@routes.get("/{topic_id}/answers", response_model=List[schemas.AnswerResponse], status_code=200)
def topic_answers(topic_id: int, db: Session = Depends(get_db)):
    return crud.get_answers(db=db, topic_id=topic_id)