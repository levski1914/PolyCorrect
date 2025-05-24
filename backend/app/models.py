from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from .database import Base

class TextEntry(Base):
    __tablename__="text_entries"

    id=Column(Integer,primary_key=True,index=True)
    content=Column(Text,nullable=False)
    issues=Column(JSON,nullable=True)
    created_at=Column(DateTime,default=datetime.utcnow)
    