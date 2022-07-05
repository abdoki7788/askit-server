from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from . import crud, models, schemas
from db_config import SessionLocal, engine


routes = APIRouter()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@routes.post("/topics/", response_model=schemas.TopicResponse, status_code=201)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    return crud.create_topic(db=db, topic=topic)

@routes.get("/topics/", response_model=List[schemas.TopicResponse], status_code=200)
def topics(db: Session = Depends(get_db)):
    return crud.get_topics(db=db)

@routes.get("/topics/{topic_id}", response_model=schemas.TopicResponse, status_code=200)
def topics(topic_id: int, db: Session = Depends(get_db)):
    return crud.get_topic(db=db, topic_id=topic_id)

@routes.delete("/topics/{topic_id}", status_code=204)
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.delete_topic(db=db, topic_id=topic_id)

@routes.patch("/topics/{topic_id}/voteup", status_code=200)
def voteup_topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.voteup_topic(db=db, topic_id=topic_id)

@routes.patch("/topics/{topic_id}/votedown", status_code=200)
def votedown_topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.votedown_topic(db=db, topic_id=topic_id)