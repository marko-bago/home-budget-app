from fastapi import APIRouter, status, Depends, HTTPException
from src.dependencies import get_session, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from datetime import datetime
from sqlalchemy import select, update
from .schemas import BalanceIn, BalanceOut
from src.auth.schemas import UserOut

router = APIRouter()

@router.get("/user_info", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user_info(
    user=Depends(get_current_user)
):
    return {"id": user.id, "username": user.username, "email": user.email}


@router.get("/balance", response_model=BalanceOut, status_code=status.HTTP_200_OK)
async def get_balance(
    user=Depends(get_current_user)
):
    return {"balance": user.balance}

@router.post("/balance", response_model=BalanceOut, status_code=status.HTTP_200_OK)
async def increase_balance(
    balance_in: BalanceIn,
    user=Depends(get_current_user),
    db=Depends(get_session)
):
    
    query = (
        update(User)
        .where(User.id == user.id)
        .values(balance=User.balance + balance_in.amount)
        .returning(User.id, User.balance)
    )
    result = await db.execute(query)
    updated_user = result.first()
    await db.commit()

    return {"balance": updated_user.balance}



