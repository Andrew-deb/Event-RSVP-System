# from fastapi import APIRouter, HTTPException
# from .models import EventCreate, EventResponse, Event
# from uuid import UUID

# router = APIRouter()
# eventdb = {}

# @router.post("/events/", response_model=EventResponse, status_code=201)
# def create_event(event: EventCreate):
#     new_event = Event(**event.dict())
#     eventdb[new_event.id] = new_event
#     return EventResponse(id=new_event.id, title=new_event.title, date=new_event.date, capacity=new_event.capacity)

# @router.get("/events/{event_id}", response_model=EventResponse)
# def get_event(event_id: UUID):
#     event = eventdb.get(event_id)
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found")
#     return EventResponse(id=event.id, title=event.title, date=event.date, capacity=event.capacity)

# @router.get("/events/", response_model=list[EventResponse])
# def list_events():
#     return [EventResponse(id=event.id, title=event.title, date=event.date, capacity=event.capacity) for event in eventdb.values()]
