from db_config import Base
import re
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import validates, relationship

from forum.models import Topic

associate_followers = Table(
    "user_follow",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True),
)

associate_favorites = Table(
    "user_favorite",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("favorite_id", Integer, ForeignKey("topics.id"), primary_key=True),
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)
    image_url = Column(String, nullable=True, default="/static/profile.jpeg")
    topics = relationship("Topic", back_populates="creator")
    answers = relationship("Answer", back_populates="creator")
    following = relationship(
        "User",
        lambda: associate_followers,
        primaryjoin=lambda: User.id == associate_followers.c.user_id,
        secondaryjoin=lambda: User.id == associate_followers.c.following_id,
        backref="followers",
    )
    favorites = relationship(
        "Topic",
        lambda: associate_favorites,
        primaryjoin=lambda: User.id == associate_favorites.c.user_id,
        secondaryjoin=lambda: Topic.id == associate_favorites.c.favorite_id,
    )
    about = Column(String, nullable=True)

    @validates('username')
    def validate_username(self, key, username):
        if re.fullmatch(r"^[a-z0-9_-]{3,15}$", username) is None:
            raise ValueError('Username must be at least 3 characters long and contain only letters, numbers, underscores, and dashes.')
        return username
    
    @validates('full_name')
    def validate_full_name(self, key, full_name):
        if re.fullmatch(r"^[a-zA-Z ]{3,30}$", full_name) is None:
            raise ValueError('Full name must be at least 3 characters long and contain only letters.')
        return full_name
    
    @validates('email')
    def validate_email(self, key, email):
        if re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is None:
            raise ValueError('Email must be a valid email address.')
        return email
    
    def __str__(self) -> str:
        return super().__str__() + f"({self.username})"