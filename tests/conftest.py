import os
import sys
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user(db):
    from app.users.models import User
    user = User(id=uuid4(), username="testuser", email="test@example.com", password="hashedpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def sample_event(db, sample_user):
    from app.events.models import Event
    event = Event(id=uuid4(), title="Test Event", date=datetime.now() + timedelta(days=7), capacity=10, current_capacity=0, organizer_id=sample_user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@pytest.fixture
def sample_rsvp(db, sample_user, sample_event):
    from app.rsvps.models import RSVP
    rsvp = RSVP(id=uuid4(), event_id=sample_event.id, name="Test User", email="test@example.com", status="going")
    db.add(rsvp)
    db.commit()
    db.refresh(rsvp)
    return rsvp
