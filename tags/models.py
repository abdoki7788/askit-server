from sqlalchemy import ForeignKey, Column, Table, Integer, String
from sqlalchemy.orm import relationship
from db_config import Base


association_table = Table(
    "tags_topics",
    Base.metadata,
    Column("tags_id", ForeignKey("tags.id")),
    Column("topics_id", ForeignKey("topics.id")),
)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    topics = relationship(
        "Topic", secondary=association_table, back_populates="tags"
    )