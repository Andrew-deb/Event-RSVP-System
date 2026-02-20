from fastapi import APIRouter, status, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.rsvps.models import RSVP
from app.rsvps.schema import RSVPCreate, RSVPResponse, RSVPUpdate
from app.events.models import Event
from uuid import UUID

router = APIRouter(prefix="/events")


@router.post("/{event_id}/rsvp", response_model=RSVPResponse, status_code=status.HTTP_201_CREATED)
def create_rsvp(event_id: UUID, name: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    existing_rsvp = db.query(RSVP).filter(
        RSVP.email == email,
        RSVP.event_id == event_id  
    ).first()
    if existing_rsvp:
        raise HTTPException(status_code=400, detail="RSVP already exists for this email and event")
    
    # For simplicity, we set status as "going" by default when RSVPing
    # The requirement only mentions name and email fields for RSVP
    rsvp_status = "going"
    
    if event.capacity is not None:
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

    db_rsvp = RSVP(event_id=event_id, name=name, email=email, status=rsvp_status)
    
    db.add(db_rsvp)
    db.commit()
    db.refresh(db_rsvp)
    return RSVPResponse(
        id=db_rsvp.id,
        event_id=db_rsvp.event_id,
        name=db_rsvp.name,
        email=db_rsvp.email,
        status=db_rsvp.status
    )


@router.get("/{event_id}/rsvps", response_model=list[RSVPResponse], status_code=status.HTTP_200_OK)
def get_rsvps(event_id: UUID, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    rsvps = db.query(RSVP).filter(RSVP.event_id == event_id).all()

    return [RSVPResponse(
        id=r.id,
        event_id=r.event_id,
        name=r.name,
        email=r.email,
        status=r.status
    ) for r in rsvps]


@router.put("/{event_id}/rsvp", status_code=200)
def update_rsvp(event_id: UUID, name: str = Form(...), email: str = Form(...), status: str = Form(...), db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    existing_rsvp = db.query(RSVP).filter(
        RSVP.email == email,
        RSVP.event_id == event_id
    ).first()

    if not existing_rsvp:
        raise HTTPException(
            status_code=404,
            detail="RSVP does not exist"
        )

    if (
        status == "going"
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

    existing_rsvp.name = name
    existing_rsvp.status = status
    db.commit()
    db.refresh(existing_rsvp)
    return RSVPResponse(
        id=existing_rsvp.id,
        event_id=existing_rsvp.event_id,
        name=existing_rsvp.name,
        email=existing_rsvp.email,
        status=existing_rsvp.status
    )
