from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db_config import get_db
from . import crud, schemas
from forum.schemas import TopicListResponse

routes = APIRouter(prefix="/tags")

@routes.get("/", status_code=200, response_model=List[schemas.TagResponse])
def get_tags(db: Session = Depends(get_db)):
    return crud.get_tags(db=db)

@routes.get("/{tag_id}", status_code=200, response_model=schemas.TagResponse)
def get_tags(tag_id: int, db: Session = Depends(get_db)):
    return crud.get_tag(db=db, tag_id=tag_id)

@routes.get("/{tag_id}/topics", status_code=200, response_model=List[TopicListResponse])
def get_tags(tag_id: int, db: Session = Depends(get_db)):
    return crud.get_tag_topics(db=db, tag_id=tag_id)