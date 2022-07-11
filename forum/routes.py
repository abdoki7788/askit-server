from fastapi import APIRouter, Body, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from . import crud, schemas, utils
from auth.dependencies import oauth2_scheme, get_current_active_user
from db_config import get_db

routes = APIRouter(prefix="/topics")

@routes.post("", response_model=schemas.TopicResponse, status_code=201)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: int = Depends(get_current_active_user)):
    return crud.create_topic(db=db, topic=topic, user_id=current_user.id)

@routes.get("", response_model=List[schemas.TopicListResponse], status_code=200)
def topics(db: Session = Depends(get_db)):
    return crud.get_topics(db=db)

@routes.get("/{topic_id}", response_model=schemas.TopicResponse, status_code=200)
def topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.get_topic(db=db, topic_id=topic_id)

@routes.delete("/{topic_id}", status_code=204)
def delete_topic(topic_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: int = Depends(get_current_active_user)):
    if utils.is_topic_creator(topic_id=topic_id, user_id=current_user.id, db=db):
        return crud.delete_topic(db=db, topic_id=topic_id)
    else:
        raise HTTPException(status_code=400, detail="You are not the creator of this topic")

@routes.put("/{topic_id}", status_code=200)
def update_topic(topic_id: int, db: Session = Depends(get_db), topic: schemas.TopicUpdate = Body(), token: str = Depends(oauth2_scheme), current_user: int = Depends(get_current_active_user)):
    if utils.is_topic_creator(topic_id=topic_id, user_id=current_user.id, db=db):
        return crud.update_topic(db=db, topic_id=topic_id, topic_schema=topic)
    else:
        raise HTTPException(status_code=400, detail="You are not the creator of this topic")

@routes.patch("/{topic_id}/voteup", status_code=200)
def voteup_topic(topic_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: int = Depends(get_current_active_user)):
    return crud.voteup_topic(db=db, topic_id=topic_id, user=current_user)

@routes.patch("/{topic_id}/votedown", status_code=200)
def votedown_topic(topic_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: int = Depends(get_current_active_user)):
    return crud.votedown_topic(db=db, topic_id=topic_id, user=current_user)

@routes.post("/{topic_id}/answers", response_model=schemas.AnswerResponse, status_code=201)
def create_answer(topic_id: int, answer: schemas.AnswerCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: int = Depends(get_current_active_user)):
    return crud.create_answer(db=db, answer=answer, topic_id=topic_id, creator_id=current_user.id)

@routes.get("/{topic_id}/answers", response_model=List[schemas.AnswerResponse], status_code=200)
def topic_answers(topic_id: int, db: Session = Depends(get_db)):
    return crud.get_answers(db=db, topic_id=topic_id)