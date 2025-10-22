from fastapi.testclient import TestClient
from src.auth.security_utils import create_access_token

from fastapi import status
from .test_utils import create_test_user
from src.main import app

# Test for /signup endpoint
def test_register(client):
    """
    Test successful user signup.
    """
    response = create_test_user(client, username="testuser", email="test@example.com", password="12345")
    response_data = response.json()

    print(response_data)

def test_login(client):

    r = create_test_user(client, username="testuser", email="test@example.com", password="12345")
    print(r.json())

    form_data = {
        "username": "testuser", 
        "password": "12345"
    }
    response = client.post("/api/v1/auth/login", data=form_data)
    
    print(response.json())

client = TestClient(app)
token = create_access_token({"sub": "testuser"})

test_login(client)

