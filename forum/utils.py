from sqlalchemy.orm import Session
from . import crud

def is_topic_creator(topic_id: int, user_id: int, db: Session):
    if crud.get_topic(db=db, topic_id=topic_id).creator_id == user_id:
        return True
    else:
        return False