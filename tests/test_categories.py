from fastapi.testclient import TestClient
from src.auth.security_utils import create_access_token

from fastapi import status
from .test_utils import create_test_user, create_test_category
from src.main import app

def test_categories(client):

    form_data = {
        "username": "testuser", 
        "email": "test@gmail.com",
        "password": "12345"
    }

    r = create_test_user(client, 
                         username=form_data["username"], 
                         email=form_data["email"], 
                         password=form_data["password"])

    response = client.post("/api/v1/auth/login", data=form_data)
    token = response.json()["access_token"]
    
    category_data = {"name":"Groceries", "description":"Money spent at grocery shops"}
    r = create_test_category(client, token=token, **category_data)

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = client.get("/api/v1/categories/", headers=headers)

    print(response.json())

client = TestClient(app)
token = create_access_token({"sub": "testuser"})

test_categories(client)
