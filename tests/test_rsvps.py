import pytest
from uuid import uuid4
from datetime import datetime, timedelta


def test_user_can_rsvp_to_event(client, sample_event):
    response = client.post(f"/events/{str(sample_event.id)}/rsvp", data={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    assert response.json()["status"] == "going"


def test_user_can_mark_rsvp_as_maybe(client, sample_event):
    response = client.post(f"/events/{str(sample_event.id)}/rsvp", data={"name": "Jane Doe", "email": "jane@example.com"})
    assert response.status_code == 201


def test_cannot_rsvp_to_nonexistent_event(client):
    response = client.post(f"/events/{str(uuid4())}/rsvp", data={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 404


def test_user_cannot_rsvp_twice_to_same_event(client, sample_event):
    # First RSVP
    client.post(f"/events/{str(sample_event.id)}/rsvp", data={"name": "John Doe", "email": "john@example.com"})
    # Second RSVP with same email
    response = client.post(f"/events/{str(sample_event.id)}/rsvp", data={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 400


def test_can_view_all_rsvps_for_an_event(client, sample_event):
    # Create an RSVP first
    client.post(f"/events/{str(sample_event.id)}/rsvp", data={"name": "John Doe", "email": "john@example.com"})
    response = client.get(f"/events/{str(sample_event.id)}/rsvps")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_returns_empty_list_when_no_rsvps_exist(client, sample_event):
    response = client.get(f"/events/{str(sample_event.id)}/rsvps")
    assert response.status_code == 200
    assert response.json() == []


def test_user_can_update_their_rsvp_status(client, sample_event):
    # Create RSVP first
    client.post(f"/events/{str(sample_event.id)}/rsvp", data={"name": "John Doe", "email": "john@example.com"})
    # Update RSVP
    response = client.put(f"/events/{str(sample_event.id)}/rsvp", data={"name": "John Doe", "email": "john@example.com", "status": "maybe"})
    assert response.status_code == 200


def test_cannot_update_rsvp_that_does_not_exist(client, sample_event):
    response = client.put(f"/events/{str(sample_event.id)}/rsvp", data={"name": "Unknown User", "email": "unknown@example.com", "status": "going"})
    assert response.status_code == 404
