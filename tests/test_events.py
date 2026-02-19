"""
Test cases for Event endpoints.

Tests cover:
- Creating a new event
- Retrieving all events
- Retrieving a specific event by ID
- Handling non-existent events
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4


class TestCreateEvent:
    """Tests for POST /events/ endpoint."""

    def test_create_event_success(self, client, sample_user):
        """Test successful event creation with valid data."""
        event_data = {
            "title": "Python Conference 2024",
            "date": (datetime.now() + timedelta(days=30)).isoformat(),
            "capacity": 100,
            "organizer_id": str(sample_user.id)
        }
        
        response = client.post("/events/", json=event_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == event_data["title"]
        assert data["capacity"] == event_data["capacity"]
        assert "id" in data

    def test_create_event_without_capacity(self, client, sample_user):
        """Test event creation without capacity limit."""
        event_data = {
            "title": "Unlimited Event",
            "date": (datetime.now() + timedelta(days=30)).isoformat(),
            "capacity": None,
            "organizer_id": str(sample_user.id)
        }
        
        response = client.post("/events/", json=event_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == event_data["title"]
        assert data["capacity"] is None

    def test_create_event_missing_title(self, client, sample_user):
        """Test that creating event without title returns validation error."""
        event_data = {
            "date": (datetime.now() + timedelta(days=30)).isoformat(),
            "capacity": 100,
            "organizer_id": str(sample_user.id)
        }
        
        response = client.post("/events/", json=event_data)
        
        assert response.status_code == 422

    def test_create_event_missing_date(self, client, sample_user):
        """Test that creating event without date returns validation error."""
        event_data = {
            "title": "Test Event",
            "capacity": 100,
            "organizer_id": str(sample_user.id)
        }
        
        response = client.post("/events/", json=event_data)
        
        assert response.status_code == 422

    def test_create_event_missing_organizer(self, client):
        """Test that creating event without organizer returns validation error."""
        event_data = {
            "title": "Test Event",
            "date": (datetime.now() + timedelta(days=30)).isoformat(),
            "capacity": 100
        }
        
        response = client.post("/events/", json=event_data)
        
        assert response.status_code == 422


class TestGetAllEvents:
    """Tests for GET /events/ endpoint."""

    def test_get_all_events_empty(self, client):
        """Test getting all events when database is empty."""
        response = client.get("/events/")
        
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_events_with_data(self, client, sample_event):
        """Test getting all events when database has events."""
        response = client.get("/events/")
        
        assert response.status_code == 200
        events = response.json()
        assert len(events) == 1
        assert events[0]["title"] == sample_event.title


class TestGetEventById:
    """Tests for GET /events/{event_id} endpoint."""

    def test_get_event_by_id_success(self, client, sample_event):
        """Test getting a specific event by ID."""
        response = client.get(f"/events/{sample_event.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_event.title
        assert data["id"] == str(sample_event.id)

    def test_get_event_by_id_not_found(self, client):
        """Test that getting non-existent event returns 404."""
        fake_id = uuid4()
        response = client.get(f"/events/{fake_id}")
        
        assert response.status_code == 404
        assert "Event not found" in response.json()["detail"]
