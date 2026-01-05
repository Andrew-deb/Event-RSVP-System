from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from .models import RSVP
from .schema import RSVPCreate, RSVPResponse, RSVPUpdate
from app.events.models import Event
from uuid import UUID

router = APIRouter(prefix="/events")

@router.post("/{event_id}/rsvps", response_model=RSVPResponse, status_code=status.HTTP_201_CREATED)
def create_rsvp(event_id: UUID, rsvp: RSVPCreate):
    db: Session = SessionLocal()

    #Checking if the event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check for existing RSVP for the same user and event
    existing_rsvp = db.query(RSVP).filter(
        RSVP.user_id == rsvp.user_id,
        RSVP.event_id == event_id  
    ).first()
    if existing_rsvp:
        raise HTTPException(status_code=400, detail="RSVP already exists for this user and event")
    
    # Capacity logic
    if rsvp.status == "going" and event.capacity is not None:
        going_count = db.query(RSVP).filter(
            RSVP.event_id == event_id,
            RSVP.status == "going"
        ).count()
        if going_count >= event.capacity:
            raise HTTPException(status_code=400, detail="Event capacity reached")
        else:
            event.current_capacity += 1
            db.add(event)
            db.commit()

    db_rsvp = RSVP(user_id=rsvp.user_id, event_id=event_id, status=rsvp.status) # create new RSVP instance
    
    db.add(db_rsvp)
    db.commit()
    db.refresh(db_rsvp)
    db.close()
    return RSVPResponse(
        id=db_rsvp.id,
        user_id=db_rsvp.user_id,
        event_id=db_rsvp.event_id,
        status=db_rsvp.status
    )

@router.get("/{event_id}/rsvps", response_model=list[RSVPResponse], status_code=status.HTTP_200_OK)
def get_rsvps(event_id: UUID):
    db : Session = SessionLocal()

    try:
        #Checking if the event exists
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        #Get all RSVPs for a particular event
        rspv = db.query(RSVP).filter(RSVP.event_id == event_id).all()
    finally:
        db.close()

    return [RSVPResponse(
        id=r.id,
        user_id=r.user_id,
        event_id=r.event_id,
        status=r.status
    ) for r in rspv]

@router.put("/{event_id}/rsvp", status_code=200)
def update_rsvp(event_id: UUID, rsvp: RSVPUpdate):
    db: Session = SessionLocal()
    try:
        #Check event exists
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        #Find existing RSVP
        existing_rsvp = db.query(RSVP).filter(
            RSVP.user_id == rsvp.user_id,
            RSVP.event_id == event_id
        ).first()

        if not existing_rsvp:
            raise HTTPException(
                status_code=404,
                detail="RSVP does not exist"
            )

        #Capacity check (only if changing to 'going')
        if (
            rsvp.status == "going"
            and existing_rsvp.status != "going"
            and event.capacity is not None
        ):
            going_count = db.query(RSVP).filter(
                RSVP.event_id == event_id,
                RSVP.status == "going"
            ).count()

            if going_count >= event.capacity:
                raise HTTPException(
                    status_code=400,
                    detail="Event capacity reached"
                )
            else:
                event.current_capacity += 1
                db.add(event)
                db.commit()

        #Update status
        existing_rsvp.status = rsvp.status
        db.commit()
        db.refresh(existing_rsvp)
        return existing_rsvp
    finally:
        db.close()
