# The schema file is used to define the structure of API inputs (User, UserCreate, UserUpdate) and outputs (UserResponse).
# It uses Pydantic models to ensure data validation and serialization.

from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str

    #We create a config class to customize how the UserResponse model behaves
    class Config:
        orm_mode = True #This tells Pydantic to read data even if it is not a dict, but an ORM model (like SQLAlchemy model)