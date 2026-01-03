from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from .models import User, UserCreate, UserResponse

router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    db: Session = SessionLocal()

    #Check for duplicate emails before creating a new user
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    db_user = User(username= user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return UserResponse(id=db_user.id, username=db_user.username, email=db_user.email)
