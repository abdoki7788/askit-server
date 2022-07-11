from typing import List
from pydantic import BaseModel

class TagBase(BaseModel):
    id: int
    name: str

class TagListResponse(TagBase):

    class Config:
        orm_mode = True

from forum.schemas import TopicResponseInTag

class TagResponse(TagBase):
    topics: List[TopicResponseInTag]

    class Config:
        orm_mode = True