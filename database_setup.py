import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func

Base = declarative_base()


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    subject = Column(String(250), nullable=False)
    content = Column(String(250), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())




engine = create_engine('sqlite:///blog.db')


Base.metadata.create_all(engine)
