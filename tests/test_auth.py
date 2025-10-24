from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from datetime import timedelta

from src.main import app  # your FastAPI app
from src.auth.models import User
from src.auth.schemas import Token
from src.auth.security_utils import verify_password, create_access_token

# Mock user for tests
mock_user = User(
    id=1,
    username="testuser",
    email="test@example.com",
    hashed_password="$2b$12$abcdefghijklmnopqrstuv",  # fake hash
    balance=1000.0
)

# Mock user input
mock_user_input = {"username": "testuser", "email": "test@example.com", "password": "password123"}


def test_register_success(client):

    response = client.post("/api/v1/auth/register", json=mock_user_input)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == mock_user_input["username"]
    assert data["email"] == mock_user_input["email"]
    assert "id" in data

def test_login_success(client):

    response = client.post("/api/v1/auth/login", data={"username": "testuser", "password": "password"})
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] == "mocked_token"

def test_login_wrong_username(client):

    response = client.post("/api/v1/auth/login", data={"username": "wronguser", "password": "password"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"

def test_login_wrong_password(client):


    response = client.post("/api/v1/auth/login", data={"username": "testuser", "password": "wrongpass"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"