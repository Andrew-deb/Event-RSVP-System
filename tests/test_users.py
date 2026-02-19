"""
Test cases for User endpoints.

Tests cover:
- Creating a new user
- Creating a user with duplicate email
- Creating a user with invalid data
"""

import pytest
from uuid import uuid4


class TestCreateUser:
    """Tests for POST /users/ endpoint."""

    def test_create_user_success(self, client):
        """Test successful user creation with valid data."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert "id" in data

    def test_create_user_duplicate_email(self, client, sample_user):
        """Test that creating a user with duplicate email returns 400."""
        user_data = {
            "username": "anotheruser",
            "email": sample_user.email,  # Uses existing user's email
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 400
        assert "Email already exists" in response.json()["detail"]

    def test_create_user_missing_username(self, client):
        """Test that creating a user without username returns validation error."""
        user_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error

    def test_create_user_missing_email(self, client):
        """Test that creating a user without email returns validation error."""
        user_data = {
            "username": "testuser",
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error

    def test_create_user_missing_password(self, client):
        """Test that creating a user without password returns validation error."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error

    def test_create_user_invalid_email_format(self, client):
        """Test that creating a user with invalid email format returns validation error."""
        user_data = {
            "username": "testuser",
            "email": "not-an-email",
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error
