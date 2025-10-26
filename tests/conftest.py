import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from src.config import settings

from src.main import app
from src.database import Base
from src.dependencies import get_session
from src.auth.models import User
from src.categories.models import Category

import logging

engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Set up a logger
@pytest_asyncio.fixture(scope="session")
def logger():
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

@pytest_asyncio.fixture(scope="function")
async def async_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(async_db):
    async def override_get_session():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

from src.auth.security_utils import create_access_token

@pytest_asyncio.fixture
async def client_with_token(async_db):
    async with TestingSessionLocal() as session:
        user = User(
            username="tester",
            email="test@example.com",
            hashed_password="hashed",
            balance=1000.0,  # default balance
            categories=[Category(name=c["name"], description=c["description"]) for c in settings.DEFAULT_CATEGORIES]
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    token = create_access_token({"sub": user.username})
    
    async def override_get_session():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers={"Authorization": f"Bearer {token}"}) as ac:
        yield ac

    app.dependency_overrides.clear()