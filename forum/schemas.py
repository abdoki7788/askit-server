from typing import List
from pydantic import BaseModel
import datetime

class AnswerResponse(BaseModel):
    id: int
    content: str
    creator: str
    votes: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

class TopicResponse(BaseModel):
    id: int
    title: str
    content: str
    votes: int
    answers: List[AnswerResponse]
    creator: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

class TopicCreate(BaseModel):
    title: str
    content: str
    creator: str

    class Config:
        orm_mode = True

class AnswerCreate(BaseModel):
    content: str
    creator: str

    class Config:
        orm_mode = True

class TopicUpdate(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True
