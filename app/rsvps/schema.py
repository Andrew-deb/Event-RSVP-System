from pydantic import BaseModel
from typing import Literal
from uuid import UUID

class RSVPCreate(BaseModel):
    user_id: UUID
    status: Literal["going", "not going", "maybe"]  # Input validation

class RSVPUpdate(BaseModel):
    user_id: UUID
    status: Literal["going", "maybe", "not_going"]

class RSVPResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: Literal["going", "not going", "maybe"]

    class Config:
        orm_mode = True