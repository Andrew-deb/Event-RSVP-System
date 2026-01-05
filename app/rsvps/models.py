from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.database import Base


class RSVP(Base):
    __tablename__ = "rsvps"

    # defines a composite unique constraint that ensure a user can RSVP only once per event
    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='unique_user_event'),
        )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    status = Column(String, nullable=False)  # e.g., "going", "not going", "maybe"
