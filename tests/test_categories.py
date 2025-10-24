from fastapi import status
import pytest

@pytest.mark.asyncio
async def test_create_category(client_with_token, logger):
    payload = {"name": "Test", "description": "test category"}
    response = await client_with_token.post("/api/v1/categories/", json=payload)
    data = response.json()

    logger.info(data)
    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == "Test"
    assert data["description"] == "test category"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_categories(client_with_token, logger):
    
    response = await client_with_token.get("/api/v1/categories/")
    data = response.json()
    logger.info(data)
    assert response.status_code == status.HTTP_200_OK
    assert data[0]["name"] == "Groceries" # from preloaded categories


@pytest.mark.asyncio
async def test_update_category(client_with_token, logger):
    # create category
    create_resp = await client_with_token.post("/api/v1/categories/", json={"name": "Bills", "description": "Monthly bills"})
    cat_id = create_resp.json()["id"]

    update_payload = {"name_new": "Utilities", "description": "Updated description"}
    update_resp = await client_with_token.put(f"/api/v1/categories/{cat_id}", json=update_payload)
    data = update_resp.json()
    logger.info(data)
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

    logger.info(data)

    assert delete_resp.status_code == status.HTTP_200_OK
    assert "deleted successfully" in data["message"]