from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    location: Optional[str] = None
    capacity: Optional[int] = None
    organizer_id: UUID

class EventResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    date: datetime
    location: Optional[str] = None
    capacity: Optional[int] = None
    organizer_id: UUID

    class Config:
        orm_mode = True # This tells Pydantic to read data even if it is not a dict, but an ORM model (like SQLAlchemy model)