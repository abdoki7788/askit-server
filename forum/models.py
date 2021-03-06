from db_config import Base
from tags.models import association_table
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, UniqueConstraint, ForeignKey, Table
from sqlalchemy.orm import relationship

associate_topic_votes = Table(
    "topics_votes",
    Base.metadata,
    Column("topics_id", ForeignKey("topics.id"), nullable=True),
    Column("users_id", ForeignKey("users.id"), nullable=True),
)

associate_answer_votes = Table(
    "answers_votes",
    Base.metadata,
    Column("answers_id", ForeignKey("answers.id"), nullable=True),
    Column("users_id", ForeignKey("users.id"), nullable=True),
)

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship("User", back_populates="answers")
    votes = relationship("User", secondary=associate_answer_votes)
    votes_count = Column(Integer, default=0)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    topic = relationship("Topic", back_populates="answers")
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    votes = relationship("User", secondary=associate_topic_votes)
    votes_count = Column(Integer, default=0)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tags = relationship(
        "Tag", secondary=association_table, back_populates="topics"
    )
    creator = relationship("User", back_populates="topics")
    answers = relationship("Answer", back_populates="topic", cascade="all, delete")
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now)