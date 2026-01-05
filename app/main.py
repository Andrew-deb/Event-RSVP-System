from fastapi import FastAPI, status, HTTPException
from app.database import Base, engine
from app.users.models import User
from app.events.models import Event
from app.users.routes import router as user_router
from app.events.routes import router as event_router
from app.rsvps.routes import router as rsvp_router

app = FastAPI()


# Base.metadata.drop_all(bind=engine)  # Drop all tables
Base.metadata.create_all(bind=engine)  # Recreate them in correct order

app.include_router(user_router)  # Already has prefix="/users" in user's routes.py
app.include_router(event_router)  # Already has prefix="/events" in event's routes.py
app.include_router(rsvp_router)   # Already has prefix="/events" in rsvp's routes.py


@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"message": "Success", "status_code": status.HTTP_200_OK}