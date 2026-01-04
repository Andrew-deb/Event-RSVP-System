from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    capacity = Column(Integer)
    organizer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
