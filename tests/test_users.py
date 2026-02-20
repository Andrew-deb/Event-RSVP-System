import pytest


def test_user_can_register_with_valid_credentials(client):
    response = client.post("/users/", json={"username": "newuser", "email": "newuser@example.com", "password": "password123"})
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"


def test_user_cannot_register_with_duplicate_email(client, sample_user):
    response = client.post("/users/", json={"username": "anotheruser", "email": sample_user.email, "password": "password123"})
    assert response.status_code == 400


def test_user_cannot_register_without_username(client):
    response = client.post("/users/", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 422


def test_user_cannot_register_with_invalid_email(client):
    response = client.post("/users/", json={"username": "testuser", "email": "not-email", "password": "password123"})
    assert response.status_code == 422
