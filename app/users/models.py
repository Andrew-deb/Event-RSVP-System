# SQLAlchemy ORM Model (for database)
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4, UUID as PydanticUUID
from app.database import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

# Pydantic Models (for validation)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: PydanticUUID
    username: str
    email: str

    #We create a config class to customize how the UserResponse model behaves
    class Config:
        orm_mode = True #This tells Pydantic to read data even if it is not a dict, but an ORM model (like SQLAlchemy model)