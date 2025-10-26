from fastapi import status
import pytest
from src.config import settings

from ..utils import json_output

@pytest.mark.asyncio
async def test_create_category(client_with_token, logger):
    payload = {"name": "Test", "description": "test category"}
    response = await client_with_token.post("/api/v1/categories/", json=payload)
    data = response.json()
    json_output(logger, response)

    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == "Test"
    assert data["description"] == "test category"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_categories(client_with_token, logger):
    
    response = await client_with_token.get("/api/v1/categories/")

    json_output(logger, response)
    data = response.json()
    
    assert response.status_code == status.HTTP_200_OK
    assert data[0]["name"] == "Groceries" # from preloaded categories


@pytest.mark.asyncio
async def test_update_category(client_with_token, logger):
    # create category
    create_resp = await client_with_token.post("/api/v1/categories/", json={"name": "Bills", "description": "Monthly bills"})
    json_output(logger, create_resp)
    t = {
        "category": settings.DEFAULT_CATEGORIES[0]["name"],
        "amount": 116.0,
        "description": "New transaction",
        "type": "expense"
    }
    
    create_trans = await client_with_token.post("/api/v1/transactions/", 
                                                json=t)
    
    cat_id = create_resp.json()["id"]

    update_payload = {"name_new": "Utilities", "description": "Updated description"}
    update_resp = await client_with_token.put(f"/api/v1/categories/{cat_id}", json=update_payload)
    data = update_resp.json()
    json_output(logger, update_resp)

    assert update_resp.status_code == status.HTTP_200_OK
    assert data["name"] == "Utilities"
    assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_delete_category(client_with_token, logger):
    # create category
    create_resp = await client_with_token.post("/api/v1/categories/", json={"name": "Bills", "description": "Monthly bills"})
    cat_id = create_resp.json()["id"]

    delete_resp = await client_with_token.delete(f"/api/v1/categories/{cat_id}")
    data = delete_resp.json()

    json_output(logger, delete_resp)

    assert delete_resp.status_code == status.HTTP_200_OK
    assert "deleted successfully" in data["message"]