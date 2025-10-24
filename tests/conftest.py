import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.main import app
from src.database import Base
from src.dependencies import get_session
from fastapi.testclient import TestClient

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

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="function")
async def async_db():
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    # Drop tables after each test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
def client(async_db):
    # Override the dependency
    async def override_get_db():
        yield async_db

    app.dependency_overrides[get_session] = override_get_db

    with TestClient(app) as client:
        yield client