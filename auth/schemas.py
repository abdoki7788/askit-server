from typing import List, Union
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    about: Union[str, None] = None

class UserResponse(User):
    id: int

    class Config:
        orm_mode = True

class UserProfile(User):
    id: int
    followers: List[UserResponse]
    following: List[UserResponse]

    class Config:
        orm_mode = True

from forum.schemas import TopicInProfile

class UserMe(UserProfile):
    favorites: List[TopicInProfile]
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Union[int, None] = None