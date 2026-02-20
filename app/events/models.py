from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
    location = Column(String, nullable=True)
    flyer = Column(LargeBinary, nullable=True)  # Store flyer as binary data
    capacity = Column(Integer, nullable=True) # nullable is set to True since event may or may not have a limit
    current_capacity = Column(Integer, default=0)  # Track current number of "going" RSVPs
    organizer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
