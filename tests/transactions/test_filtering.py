from fastapi import status
from src.config import settings
from src.transactions.models import Transaction, TransactionType
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .test_crud import transaction_data, route_path
import pytest
from ..utils import json_output


@pytest.mark.asyncio
async def test_list_transactions_basic(client_with_token, logger):

    # Create transactions
    for t in transaction_data:
        logger.info("")
        r = await client_with_token.post(f"{route_path}/", json=t)
        json_output(logger, r)

    # Test listing transactions
    response = await client_with_token.get(f"{route_path}/")
    json_output(logger, r)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(transaction_data)

@pytest.mark.asyncio
async def test_list_transactions_filter_date(client_with_token, async_db, logger):

    # Create transactions directly in db
    async_db.add_all([
        Transaction(user_id=1,
                    category_id=1, 
                    amount=100.0, 
                    type=TransactionType.expense, 
                    created_at=datetime.now() - timedelta(days=1)),
        Transaction(user_id=1,
                    category_id=2, 
                    amount=200.0, 
                    type=TransactionType.income, 
                    created_at=datetime.now() - relativedelta(months=1)),
        Transaction(user_id=1,
                    category_id=3, 
                    amount=100.0, 
                    type=TransactionType.income, 
                    created_at=datetime.now() - relativedelta(months=2)),
        Transaction(user_id=1,
                    category_id=3, 
                    amount=100.0, 
                    type=TransactionType.income, 
                    created_at=datetime.now() - relativedelta(years=2)),

    ])
    await async_db.commit()

    filter_params = {
        "period": "week",
        "sort_by": "amount"
    }
    # Test listing transactions
    r = await client_with_token.get(f"{route_path}/", params=filter_params)
    json_output(logger, r)

    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()) == 1

    filter_params = {
        "period": "quarter",
        "sort_by": "amount"
    }
    # Test listing transactions
    r = await client_with_token.get(f"{route_path}/", params=filter_params)
    json_output(logger, r)

    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()) == 3

    filter_params = {
        "from_date": datetime.now().date() - relativedelta(months=1),
        "to_date": datetime.now().date() - relativedelta(days=2),
        "sort_by": "amount"
    }
    # Test listing transactions
    r = await client_with_token.get(f"{route_path}/", params=filter_params)
    json_output(logger, r)

    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()) == 1


@pytest.mark.asyncio
async def test_get_summary(client_with_token, logger):

     # Create transactions
    for t in transaction_data:
        await client_with_token.post(f"{route_path}/", json=t)

    filter_params = {
        "category": settings.DEFAULT_CATEGORIES[0]["name"],
        "amount_min": 100.0,
        "sort_by": "amount"
    }
    # Test getting transaction summary
    response = await client_with_token.get(f"{route_path}/summary", params=filter_params)
    json_output(logger, response)
    
    assert response.status_code == status.HTTP_200_OK
    summary = response.json()
    
    assert "num_of_transactions" in summary
    assert "sum_of_transactions" in summary
    assert "avg_transaction_amount" in summary

