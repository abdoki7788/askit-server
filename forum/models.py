from db_config import Base
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    creator = Column(String, nullable=False)
    votes = Column(Integer, nullable=False, default=0)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    topic = relationship("Topic", back_populates="answers")
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

class Topic(Base):
    __tablename__ = "topics"
    __table_args__ = (UniqueConstraint("title"),)
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    votes = Column(Integer, default=0)
    creator = Column(String)
    answers = relationship("Answer", back_populates="topic", cascade="all, delete")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.datetime.now()