from pydantic import BaseModel
from typing import Literal
from uuid import UUID

class RSVPCreate(BaseModel):
    name: str
    email: str

class RSVPUpdate(BaseModel):
    name: str
    email: str
    status: Literal["going", "maybe", "not_going"]

class RSVPResponse(BaseModel):
    id: UUID
    event_id: UUID
    name: str
    email: str
    status: str

    class Config:
        orm_mode = True