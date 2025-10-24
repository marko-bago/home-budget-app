
from .config import settings

from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.transactions.router import router as transactions_router
from src.categories.router import router as categories_router
from src.profiles.router import router as profile_router
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import Base, engine

## Needed for lifespan table creation
from src.transactions.models import Transaction
from src.auth.models import User
from src.categories.models import Category

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Set all CORS enabled origins
if settings.ALL_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALL_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(auth_router, prefix=f"/api/{settings.VERSION}/auth")
app.include_router(transactions_router, prefix=f"/api/{settings.VERSION}/transactions")
app.include_router(categories_router, prefix=f"/api/{settings.VERSION}/categories")
app.include_router(profile_router, prefix=f"/api/{settings.VERSION}/profile")


    