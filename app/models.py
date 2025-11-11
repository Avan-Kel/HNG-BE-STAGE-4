from sqlalchemy import Column, String, Integer, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base

class Template(Base):
    __tablename__ = "templates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    subject = Column(String)
    body = Column(String)
    language = Column(String)