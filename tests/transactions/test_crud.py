from fastapi import status
from src.config import settings
from ..utils import json_output

import pytest

route_path = f"api/{settings.VERSION}/transactions"

# Test creating a transaction
transaction_data = [
    {
        "category": settings.DEFAULT_CATEGORIES[0]["name"],
        "amount": 116.0,
        "description": "New transaction",
        "type": "expense"
    },
    {
        "category": settings.DEFAULT_CATEGORIES[0]["name"],
        "amount": 112.0,
        "description": "New transaction",
        "type": "expense"
    },
    {
        "category": settings.DEFAULT_CATEGORIES[0]["name"],
        "amount": 98.0,
        "description": "New transaction",
        "type": "expense"
    },
    {
        "category": settings.DEFAULT_CATEGORIES[1]["name"],
        "amount": 15.0,
        "description": "New transaction",
        "type": "expense"
    },
    {
        "category": settings.DEFAULT_CATEGORIES[1]["name"],
        "amount": 40.0,
        "description": "New transaction",
        "type": "expense"
    },
    {
        "category": settings.DEFAULT_CATEGORIES[2]["name"],
        "amount": 50.0,
        "description": "New transaction",
        "type": "expense"
    },
    {
        "category": settings.DEFAULT_CATEGORIES[3]["name"],
        "amount": 19.99,
        "description": "New transaction",
        "type": "expense"
    },
    {
        "category": settings.DEFAULT_CATEGORIES[4]["name"],
        "amount": 86.0,
        "description": "New transaction",
        "type": "expense"
    }
]


@pytest.mark.asyncio
async def test_create_transaction(client_with_token, logger):

    response = await client_with_token.post(f"{route_path}/", json=transaction_data[0])
    
    assert response.status_code == status.HTTP_200_OK
    transaction = response.json()
    json_output(logger, response)
    assert transaction["amount"] == transaction_data[0]["amount"]
    assert transaction["description"] == transaction_data[0]["description"]

@pytest.mark.asyncio
async def test_get_transaction_by_id(client_with_token, logger):

    response = await client_with_token.post(f"{route_path}/", json=transaction_data[0])
    response = await client_with_token.get(f"{route_path}/1")
    
    assert response.status_code == status.HTTP_200_OK
    json_output(logger, response)


@pytest.mark.asyncio
async def test_update_transaction(client_with_token, logger):

    # Create transaction
    response = await client_with_token.post(f"{route_path}/", json=transaction_data[0])
    json_output(logger, response)

    # Test updating a transaction
    transaction_update_data = {
        "category_new": "Electronics",
        "description_new": "Updated transaction category"
    }

    response = await client_with_token.put(f"{route_path}/1", json=transaction_update_data)
    
    assert response.status_code == status.HTTP_200_OK
    updated_transaction = response.json()
    json_output(logger, response)
    assert updated_transaction["category"]["name"] == transaction_update_data["category_new"]
    assert updated_transaction["description"] == transaction_update_data["description_new"]


@pytest.mark.asyncio
async def test_delete_transaction(client_with_token):

    # Create transaction
    await client_with_token.post(f"{route_path}/", json=transaction_data[0])

    # Test deleting a transaction
    response = await client_with_token.delete(f"{route_path}/1")
    
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert "message" in result
    assert "Transaction '1' deleted successfully." in result["message"]