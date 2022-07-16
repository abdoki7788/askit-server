from typing import List, Union
from pydantic import BaseModel, PrivateAttr
import datetime

class TopicBase(BaseModel):
    title: str
    content: str

class TopicInProfile(TopicBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tags: List
    class Config:
        orm_mode = True

from auth.schemas import UserResponse

class TopicResponseInTag(TopicBase):
    id: int
    slug: str
    creator: UserResponse
    votes: List[UserResponse]
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class AnswerResponse(BaseModel):
    id: int
    content: str
    creator: UserResponse
    votes: List[UserResponse]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

from tags.schemas import TagListResponse

class TopicResponse(TopicBase):
    id: int
    slug: str
    votes: List[UserResponse]
    tags: List[TagListResponse]
    answers: List[AnswerResponse]
    creator: UserResponse
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

class TopicListResponse(TopicBase):
    id: int
    slug: str
    votes: List[UserResponse]
    tags: List[TagListResponse]
    creator: UserResponse
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class TopicCreate(TopicBase):
    tags: List[str]
    class Config:
        orm_mode = True

class AnswerCreate(BaseModel):
    content: str

    class Config:
        orm_mode = True

class TopicUpdate(TopicBase):

    class Config:
        orm_mode = True