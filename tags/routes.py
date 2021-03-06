from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db_config import get_db
from . import crud, schemas
from forum.schemas import TopicResponseInTag

routes = APIRouter(prefix="/tags", tags=["tags"])

@routes.get("/", status_code=200, response_model=List[schemas.TagListResponse])
def get_tags(db: Session = Depends(get_db)):
    return crud.get_tags(db=db)

@routes.post("/", status_code=201, response_model=schemas.TagListResponse)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db=db, tag=tag)

@routes.get("/{tag_id}", status_code=200, response_model=schemas.TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    return crud.get_tag(db=db, tag_id=tag_id)

@routes.get("/{tag_id}/topics", status_code=200, response_model=List[TopicResponseInTag])
def get_tag_topics(tag_id: int, db: Session = Depends(get_db)):
    return crud.get_tag_topics(db=db, tag_id=tag_id)