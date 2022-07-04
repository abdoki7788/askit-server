from pydantic import BaseModel
import datetime

class TopicResponse(BaseModel):
    id: int
    title: str
    content: str
    votes: int
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