from typing import List, Union
from pydantic import BaseModel, PrivateAttr
import datetime
from auth.schemas import UserResponse

class TopicBase(BaseModel):
    title: str
    content: str

class TopicResponseInTag(TopicBase):
    id: int
    creator: UserResponse
    votes: int
    created_at: datetime.datetime

class AnswerResponse(BaseModel):
    id: int
    content: str
    creator: UserResponse
    votes: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

from tags.schemas import TagResponse

class TopicResponse(TopicBase):
    id: int
    votes: int
    tags: List[TagResponse]
    answers: List[AnswerResponse]
    creator: UserResponse
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

class TopicListResponse(TopicBase):
    id: int
    votes: int
    tags: List[TagResponse]
    creator: UserResponse
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class TopicCreate(TopicBase):

    class Config:
        orm_mode = True

class AnswerCreate(BaseModel):
    content: str

    class Config:
        orm_mode = True

class TopicUpdate(TopicBase):

    class Config:
        orm_mode = True