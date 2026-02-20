from fastapi import APIRouter, status, HTTPException, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.events.models import Event
from app.events.schema import EventCreate, EventResponse
from uuid import UUID
from datetime import datetime

router = APIRouter(prefix="/events")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EventResponse)
async def create_event(
    title: str = Form(...),
    description: str = Form(None),
    date: str = Form(...),
    location: str = Form(None),
    capacity: int = Form(None),
    organizer_id: str = Form(...),
    flyer: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Parse date from string
    try:
        event_date = datetime.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO 8601 format.")
    
    # Parse organizer_id from string to UUID
    from uuid import UUID
    try:
        org_id = UUID(organizer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid organizer_id format. Must be a valid UUID.")
    
    # Handle flyer file
    flyer_data = None
    if flyer:
        flyer_data = await flyer.read()
    
    db_event = Event(
        title=title,
        description=description,
        date=event_date,
        location=location,
        capacity=capacity,
        organizer_id=org_id,
        flyer=flyer_data,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return EventResponse(
        id=db_event.id,
        title=db_event.title,
        description=db_event.description,
        date=db_event.date,
        location=db_event.location,
        capacity=db_event.capacity,
        organizer_id=db_event.organizer_id
    )


@router.get("/", response_model=list[EventResponse])
def get_all_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return [EventResponse(
        id=event.id,
        title=event.title,
        date=event.date,
        capacity=event.capacity,
        organizer_id=event.organizer_id
    ) for event in events]


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: UUID, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return EventResponse(
        id=event.id,
        title=event.title,
        date=event.date,
        current_capacity=event.current_capacity,
        capacity=event.capacity,
        organizer_id=event.organizer_id
    )
