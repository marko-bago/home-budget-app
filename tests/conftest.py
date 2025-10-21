import pytest
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.main import app
from src.expenses.models import ExpenseCategory 
from src.auth.models import User 
from src.auth.security import hash_password
from src.database import Base

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

FIXED_CATEGORIES = [
    {"name": "Groceries", "description": "Money spent at grocery shops"},
    {"name": "Transport", "description": "Gas, public transit, and ride shares"},
    {"name": "Housing", "description": "Rent/Mortgage and utilities"},
    {"name": "Dining", "description": "Restaurants, street food, ordering take-out"},
    {"name": "Drinks", "description": "Going out for coffee, alcohol or other drinks"},
    {"name": "Fashion", "description": "Clothes, shoes, fashion accessories"},
    {"name": "Education", "description": "Education cost, seminars, webinars, courses"},
    {"name": "Tech", "description": "Machines, gadgets, tools, computers and such"},
    {"name": "Subscriptions", "description": "Netflix, Spotify, Youtube and so on"},
    {"name": "Other", "description": "Everything else"},
]



# Setup async test database
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Override db dependency
async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[lambda: TestingSessionLocal()] = override_get_session

@pytest.fixture(scope="module")
async def async_client():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def create_user():
    async with TestingSessionLocal() as session:
        user = User(
            username="testuser",
            email="testuser@example.com",
            hashed_password=hash_password("password123"),
            is_superuser=True
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

@pytest.fixture
async def seed_categories():
    async with TestingSessionLocal() as session:
        categories = [
            ExpenseCategory(name="Food"),
            ExpenseCategory(name="Transport"),
            ExpenseCategory(name="Entertainment")
        ]
        session.add_all(categories)
        await session.commit()
        return categories

@pytest.mark.asyncio
async def test_create_expenses(async_client: AsyncClient, create_user, seed_categories):
    # Normally you would obtain a JWT token from login
    # For simplicity, assume you have a helper to create token
    from src.auth.security import create_access_token
    token = create_access_token({"sub": create_user.username})

    headers = {"Authorization": f"Bearer {token}"}

    # Create a couple of expenses
    expense_data = [
        {"category_id": seed_categories[0].id, "amount": 20.5, "description": "Lunch"},
        {"category_id": seed_categories[1].id, "amount": 15.0, "description": "Taxi"}
    ]

    for data in expense_data:
        response = await async_client.post("/expenses/create", json=data, headers=headers)
        assert response.status_code == 200
        assert response.json()["amount"] == data["amount"]

    # List expenses and check
    response = await async_client.get("/expenses/", headers=headers)
    assert response.status_code == 200
    expenses = response.json()
    assert len(expenses) == 2
    assert expenses[0]["description"] == "Lunch" or expenses[1]["description"] == "Lunch"




