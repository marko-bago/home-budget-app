from fastapi import APIRouter, Depends
from .schemas import ExpenseCreate
from src.dependencies import db_dependency, user_dependency
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from .models import Expense
from datetime import datetime

router = APIRouter()

@router.post("/create", response_model=None)
async def create_expense(
    expense_in: ExpenseCreate, 
    user = user_dependency,
    db = db_dependency,
):
    new_expense = Expense(
        user_id=user.id,
        category_id=expense_in.category_id,
        amount=expense_in.amount,
        description=expense_in.description,
        spent_at=datetime.now()
    )

    await db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)

    return {"message": f"Expense ${new_expense.amount} added."}
