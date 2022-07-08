from fastapi import APIRouter, Body, Depends
from typing import List
from sqlalchemy.orm import Session
from . import crud, schemas
from db_config import get_db

routes = APIRouter()

@routes.post("/topics", response_model=schemas.TopicResponse, status_code=201)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    return crud.create_topic(db=db, topic=topic)

@routes.get("/topics", response_model=List[schemas.TopicListResponse], status_code=200)
def topics(db: Session = Depends(get_db)):
    return crud.get_topics(db=db)

@routes.get("/topics/{topic_id}", response_model=schemas.TopicResponse, status_code=200)
def topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.get_topic(db=db, topic_id=topic_id)

@routes.delete("/topics/{topic_id}", status_code=204)
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.delete_topic(db=db, topic_id=topic_id)

@routes.put("/topics/{topic_id}", status_code=200)
def update_topic(topic_id: int, db: Session = Depends(get_db), topic: schemas.TopicUpdate = Body()):
    return crud.update_topic(db=db, topic_id=topic_id, topic_schema=topic)

@routes.patch("/topics/{topic_id}/voteup", status_code=200)
def voteup_topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.voteup_topic(db=db, topic_id=topic_id)

@routes.patch("/topics/{topic_id}/votedown", status_code=200)
def votedown_topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.votedown_topic(db=db, topic_id=topic_id)

@routes.post("/topics/{topic_id}/answers", response_model=schemas.AnswerResponse, status_code=201)
def create_answer(topic_id: int, answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    return crud.create_answer(db=db, answer=answer, topic_id=topic_id)

@routes.get("/topics/{topic_id}/answers", response_model=List[schemas.AnswerResponse], status_code=200)
def topic_answers(topic_id: int, db: Session = Depends(get_db)):
    return crud.get_answers(db=db, topic_id=topic_id)