from typing import List, Union
from pydantic import BaseModel, PrivateAttr
import datetime
from auth.schemas import UserResponse

class AnswerResponse(BaseModel):
    id: int
    content: str
    creator: UserResponse
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
    creator: UserResponse
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

class TopicListResponse(BaseModel):
    id: int
    title: str
    content: str
    votes: int
    creator: UserResponse
    created_at: datetime.datetime
    answers_count: int

    class Config:
        orm_mode = True

class TopicCreate(BaseModel):
    title: str
    content: str
    creator_id: int

    class Config:
        orm_mode = True

class AnswerCreate(BaseModel):
    content: str
    creator: UserResponse

    class Config:
        orm_mode = True

class TopicUpdate(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True
