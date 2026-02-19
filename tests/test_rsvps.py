"""
Test cases for RSVP endpoints.

Tests cover:
- Creating a new RSVP
- Getting RSVPs for an event
- Updating RSVP status
- Handling duplicate RSVPs
- Handling capacity limits
"""

import pytest
from uuid import uuid4
from datetime import datetime, timedelta


class TestCreateRSVP:
    """Tests for POST /events/{event_id}/rsvps endpoint."""

    def test_create_rsvp_success(self, client, sample_user, sample_event):
        """Test successful RSVP creation with 'going' status."""
        rsvp_data = {
            "user_id": str(sample_user.id),
            "status": "going"
        }
        
        response = client.post(f"/events/{sample_event.id}/rsvps", json=rsvp_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == str(sample_user.id)
        assert data["status"] == "going"
        assert data["event_id"] == str(sample_event.id)

    def test_create_rsvp_maybe_status(self, client, sample_user, sample_event):
        """Test creating RSVP with 'maybe' status."""
        # Create another user for this test
        from app.users.models import User
        new_user = User(
            id=uuid4(),
            username="anotheruser",
            email="another@example.com",
            password="password"
        )
        client.app.database.SessionLocal().add(new_user)
        client.app.database.SessionLocal().commit()
        
        rsvp_data = {
            "user_id": str(new_user.id),
            "status": "maybe"
        }
        
        response = client.post(f"/events/{sample_event.id}/rsvps", json=rsvp_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "maybe"

    def test_create_rsvp_not_going_status(self, client, sample_user, sample_event):
        """Test creating RSVP with 'not going' status."""
        # Create another user for this test
        from app.users.models import User
        new_user = User(
            id=uuid4(),
            username="thirduser",
            email="third@example.com",
            password="password"
        )
        client.app.database.SessionLocal().add(new_user)
        client.app.database.SessionLocal().commit()
        
        rsvp_data = {
            "user_id": str(new_user.id),
            "status": "not going"
        }
        
        response = client.post(f"/events/{sample_event.id}/rsvps", json=rsvp_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "not going"

    def test_create_rsvp_event_not_found(self, client, sample_user):
        """Test that creating RSVP for non-existent event returns 404."""
        fake_event_id = uuid4()
        rsvp_data = {
            "user_id": str(sample_user.id),
            "status": "going"
        }
        
        response = client.post(f"/events/{fake_event_id}/rsvps", json=rsvp_data)
        
        assert response.status_code == 404
        assert "Event not found" in response.json()["detail"]

    def test_create_rsvp_duplicate(self, client, sample_user, sample_rsvp):
        """Test that creating duplicate RSVP returns 400."""
        rsvp_data = {
            "user_id": str(sample_rsvp.user_id),
            "status": "going"
        }
        
        response = client.post(f"/events/{sample_rsvp.event_id}/rsvps", json=rsvp_data)
        
        assert response.status_code == 400
        assert "RSVP already exists" in response.json()["detail"]

    def test_create_rsvp_capacity_reached(self, client, sample_user, sample_event):
        """Test that creating RSVP when capacity is reached returns 400."""
        # First, update the event to have capacity of 1
        from app.events.models import Event
        db = client.app.database.SessionLocal()
        event = db.query(Event).filter(Event.id == sample_event.id).first()
        event.capacity = 1
        db.commit()
        
        # Try to create a second RSVP (first one was created by sample_rsvp fixture)
        from app.users.models import User
        new_user = User(
            id=uuid4(),
            username="capacityuser",
            email="capacity@example.com",
            password="password"
        )
        db.add(new_user)
        db.commit()
        
        rsvp_data = {
            "user_id": str(new_user.id),
            "status": "going"
        }
        
        response = client.post(f"/events/{sample_event.id}/rsvps", json=rsvp_data)
        
        assert response.status_code == 400
        assert "capacity" in response.json()["detail"].lower()


class TestGetRSVPs:
    """Tests for GET /events/{event_id}/rsvps endpoint."""

    def test_get_rsvps_for_event(self, client, sample_rsvp):
        """Test getting all RSVPs for an event."""
        response = client.get(f"/events/{sample_rsvp.event_id}/rsvps")
        
        assert response.status_code == 200
        rsvps = response.json()
        assert len(rsvps) == 1
        assert rsvps[0]["id"] == str(sample_rsvp.id)

    def test_get_rsvps_event_not_found(self, client):
        """Test that getting RSVPs for non-existent event returns 404."""
        fake_event_id = uuid4()
        
        response = client.get(f"/events/{fake_event_id}/rsvps")
        
        assert response.status_code == 404
        assert "Event not found" in response.json()["detail"]

    def test_get_rsvps_empty(self, client, sample_event):
        """Test getting RSVPs when no RSVPs exist for event."""
        response = client.get(f"/events/{sample_event.id}/rsvps")
        
        assert response.status_code == 200
        assert response.json() == []


class TestUpdateRSVP:
    """Tests for PUT /events/{event_id}/rsvp endpoint."""

    def test_update_rsvp_success(self, client, sample_rsvp):
        """Test successful RSVP status update."""
        rsvp_data = {
            "user_id": str(sample_rsvp.user_id),
            "status": "maybe"
        }
        
        response = client.put(f"/events/{sample_rsvp.event_id}/rsvps", json=rsvp_data)
        
        assert response.status_code == 200

    def test_update_rsvp_event_not_found(self, client, sample_user):
        """Test that updating RSVP for non-existent event returns 404."""
        fake_event_id = uuid4()
        rsvp_data = {
            "user_id": str(sample_user.id),
            "status": "going"
        }
        
        response = client.put(f"/events/{fake_event_id}/rsvps", json=rsvp_data)
        
        assert response.status_code == 404
        assert "Event not found" in response.json()["detail"]

    def test_update_rsvp_not_found(self, client, sample_event, sample_user):
        """Test that updating non-existent RSVP returns 404."""
        rsvp_data = {
            "user_id": str(sample_user.id),
            "status": "going"
        }
        
        response = client.put(f"/events/{sample_event.id}/rsvps", json=rsvp_data)
        
        assert response.status_code == 404
        assert "RSVP does not exist" in response.json()["detail"]
