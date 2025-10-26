from fastapi import status
from src.config import settings
import pytest

api_route_path = f"api/{settings.VERSION}"


# Test creating a transaction
transaction_data = [
    {
        "category": settings.DEFAULT_CATEGORIES[0]["name"],
        "amount": 600.0,
        "description": "New transaction",
        "type": "expense"
    },
    {
        "category": settings.DEFAULT_CATEGORIES[1]["name"],
        "amount": 1000.0,
        "description": "New transaction",
        "type": "expense"
    },
    {
        "category": settings.DEFAULT_CATEGORIES[2]["name"],
        "amount": 2000.0,
        "description": "Payment",
        "type": "income"
    }

]

@pytest.mark.asyncio
async def test_balance(client_with_token, logger):

    r = await client_with_token.post(f"{api_route_path}/transactions/", json=transaction_data[0])
    r = await client_with_token.get(f"{api_route_path}/profile/")
    assert r.status_code == status.HTTP_200_OK
    assert r.json()["balance"] == 400.0

    r = await client_with_token.post(f"{api_route_path}/transactions/", json=transaction_data[1])
    assert r.status_code == status.HTTP_409_CONFLICT
    assert r.json()["detail"] == 'Insufficient balance.'

    r = await client_with_token.get(f"{api_route_path}/profile/")
    assert r.status_code == status.HTTP_200_OK
    assert r.json()["balance"] == 400.0

    r = await client_with_token.post(f"{api_route_path}/transactions/", json=transaction_data[2])
    r = await client_with_token.get(f"{api_route_path}/profile/")
    assert r.status_code == status.HTTP_200_OK
    assert r.json()["balance"] == 2400.0

        
