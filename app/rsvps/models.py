from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.database import Base


class RSVP(Base):
    __tablename__ = "rsvps"

    # defines a composite unique constraint that ensure a user can RSVP only once per event
    __table_args__ = (
        UniqueConstraint('event_id', 'email', name='unique_event_email'),
        )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(String, nullable=False)  # e.g., "going", "not going", "maybe"
