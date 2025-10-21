
from .config import settings

from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.expenses.router import router as expenses_router
from starlette.middleware.cors import CORSMiddleware
from src.expenses.models import Expense
from src.auth.models import User
from src.database import engine

import asyncio


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
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
app.include_router(expenses_router, prefix=f"/api/{settings.VERSION}/expenses")