import pytest
from datetime import datetime, timedelta
from uuid import uuid4


def test_organizer_can_create_event_with_valid_details(client, sample_user):
    response = client.post("/events/", data={"title": "Python Conference", "date": (datetime.now() + timedelta(days=30)).isoformat(), "capacity": 100, "organizer_id": str(sample_user.id)})
    assert response.status_code == 201
    assert response.json()["title"] == "Python Conference"


def test_organizer_can_create_event_without_capacity_limit(client, sample_user):
    response = client.post("/events/", data={"title": "Unlimited Event", "date": (datetime.now() + timedelta(days=30)).isoformat(), "organizer_id": str(sample_user.id)})
    assert response.status_code == 201


def test_organizer_cannot_create_event_without_title(client, sample_user):
    response = client.post("/events/", data={"date": (datetime.now() + timedelta(days=30)).isoformat(), "capacity": 100})
    assert response.status_code == 422


def test_can_retrieve_all_events_when_none_exist(client):
    response = client.get("/events/")
    assert response.status_code == 200
    assert response.json() == []


def test_can_retrieve_all_events_when_events_exist(client, sample_event):
    response = client.get("/events/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_can_retrieve_specific_event_by_id(client, sample_event):
    response = client.get(f"/events/{str(sample_event.id)}")
    assert response.status_code == 200
    assert response.json()["title"] == sample_event.title


def test_cannot_retrieve_nonexistent_event(client):
    response = client.get(f"/events/{str(uuid4())}")
    assert response.status_code == 404

def test_organizer_cannot_create_event_with_invalid_date_format(client, sample_user):
    response = client.post("/events/", data={"title": "Test Event", "date": "invalid-date", "organizer_id": str(sample_user.id)})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid date format. Use ISO 8601 format."

def test_organizer_cannot_create_event_with_invalid_uuid_format(client):

    response = client.post("/events/", data={"title": "Test Event", "date": (datetime.now() + timedelta(days=30)).isoformat(), "organizer_id": "invalid-uuid"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid organizer_id format. Must be a valid UUID."
