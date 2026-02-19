"""
Test configuration and fixtures for the Event RSVP System.

This module provides reusable test fixtures including:
- Test client for API testing
- Test database session
- Sample data fixtures
"""

import os
import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test database URL before importing app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.database import Base
from app.main import app
from app.users.models import User
from app.events.models import Event
from app.rsvps.models import RSVP
from app.database import SessionLocal


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database."""
    from app.database import SessionLocal
    
    # Override the get_db dependency
    from app.main import app
    app.dependency_overrides[SessionLocal] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        id=uuid4(),
        username="testuser",
        email="test@example.com",
        password="hashedpassword"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_event(db_session, sample_user):
    """Create a sample event for testing."""
    event = Event(
        id=uuid4(),
        title="Test Event",
        date=datetime.now() + timedelta(days=7),
        capacity=10,
        current_capacity=0,
        organizer_id=sample_user.id
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event


@pytest.fixture
def sample_rsvp(db_session, sample_user, sample_event):
    """Create a sample RSVP for testing."""
    rsvp = RSVP(
        id=uuid4(),
        user_id=sample_user.id,
        event_id=sample_event.id,
        status="going"
    )
    db_session.add(rsvp)
    db_session.commit()
    db_session.refresh(rsvp)
    return rsvp
