from fastapi import status

import pytest

# Mock user input
mock_user_input = {"username": "testuser", "email": "test@example.com", "password": "password123"}

@pytest.mark.asyncio
async def test_register_success(client, logger):

    response = await client.post("/api/v1/auth/register", json=mock_user_input)

    data = response.json()
    logger.info(data)

    assert response.status_code == status.HTTP_201_CREATED
    assert data["username"] == mock_user_input["username"]
    assert data["email"] == mock_user_input["email"]
    assert "id" in data

@pytest.mark.asyncio
async def test_register_username_taken(client, logger):

    response = await client.post("/api/v1/auth/register", json=mock_user_input)
    response = await client.post("/api/v1/auth/register", json=mock_user_input)
    data = response.json()
    logger.info(data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_login_success(client, logger):

    await client.post("/api/v1/auth/register", json=mock_user_input)

    response = await client.post("/api/v1/auth/login", 
                                 data={"username":mock_user_input["username"],
                                       "password": mock_user_input["password"]})
    
    data = response.json()
    logger.info(data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_username(client, logger):

    response = await client.post("/api/v1/auth/login", data={"username": "wronguser", "password": "password"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_login_wrong_password(client, logger):


    response = await client.post("/api/v1/auth/login", data={"username": "testuser", "password": "wrongpass"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"
