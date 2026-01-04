from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from .models import Event
from .schema import EventCreate, EventResponse

router = APIRouter(prefix="/events")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EventResponse)
def create_event(event: EventCreate):
    db: Session = SessionLocal()

    db_event = Event(
        title=event.title,
        date=event.date,
        capacity=event.capacity,
        organizer_id=event.organizer_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    db.close()
    return EventResponse(
        id=db_event.id,
        title=db_event.title,
        date=db_event.date,
        capacity=db_event.capacity,
        organizer_id=db_event.organizer_id
    )

@router.get("/", response_model=list[EventResponse])
def get_all_events():
    db: Session = SessionLocal() # Create a new database session

    try:
        events = db.query(Event).all()

        return [EventResponse(
            id=event.id,
            title=event.title,
            date=event.date,
            capacity=event.capacity,
            organizer_id=event.organizer_id
        ) for event in events] # Convert each Event to EventResponse and return the list of each EventResponse
    finally:
        db.close()

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id):
    db: Session = SessionLocal()

    try:
        event = db.query(Event).filter(Event.id == event_id).first() # Get the event with the specified ID using the filter method
        
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        return EventResponse(
            id=event.id,
            title=event.title,
            date=event.date,
            capacity=event.capacity,
            organizer_id=event.organizer_id
        )
    finally:
        db.close()