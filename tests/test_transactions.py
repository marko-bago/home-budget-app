from fastapi import status
from src.config import settings
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
async def test_list_transactions_basic(client_with_token, logger):

    # Create transactions
    for t in transaction_data:
        r = await client_with_token.post(f"{route_path}/", json=t)
        logger.info(r.json())

    # Test listing transactions
    response = await client_with_token.get(f"{route_path}/")
    logger.info(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(transaction_data)

@pytest.mark.asyncio
async def test_list_transactions_filter(client_with_token, logger):

    # Create transactions
    for t in transaction_data:
        await client_with_token.post(f"{route_path}/", json=t)

    filter_params = {
        "category": settings.DEFAULT_CATEGORIES[0]["name"],
        "amount_min": 100.0,
        "sort_by": "amount"
    }
    # Test listing transactions
    response = await client_with_token.get(f"{route_path}/", params=filter_params)
    logger.info(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_summary(client_with_token, logger):

     # Create transactions
    for t in transaction_data:
        await client_with_token.post(f"{route_path}/", json=t)

    filter_params = {
        #"category": settings.DEFAULT_CATEGORIES[0]["name"],
        #"amount_min": 100.0,
        "sort_by": "amount"
    }
    # Test getting transaction summary
    response = await client_with_token.get(f"{route_path}/summary", params=filter_params)
    
    assert response.status_code == status.HTTP_200_OK
    summary = response.json()
    logger.info(summary)
    assert "num_of_transactions" in summary
    assert "sum_of_transactions" in summary
    assert "avg_transaction_amount" in summary


@pytest.mark.asyncio
async def test_create_transaction(client_with_token, logger):

    response = await client_with_token.post(f"{route_path}/", json=transaction_data[0])
    
    assert response.status_code == status.HTTP_200_OK
    transaction = response.json()
    logger.info(transaction)
    assert transaction["amount"] == transaction_data[0]["amount"]


@pytest.mark.asyncio
async def test_update_transaction(client_with_token, logger):

    # Create transaction
    await client_with_token.post(f"{route_path}/", json=transaction_data[0])

    # Test updating a transaction
    transaction_update_data = {
        "category_new": "Electronics",
        "amount_new": 200.0,
        "description": "Updated transaction data"
    }

    response = await client_with_token.put(f"{route_path}/1", json=transaction_update_data)
    
    assert response.status_code == status.HTTP_200_OK
    updated_transaction = response.json()
    logger.info(updated_transaction)
    assert updated_transaction["amount"] == transaction_update_data["amount_new"]


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