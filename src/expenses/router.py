from fastapi import APIRouter, status, Depends
from .schemas import ExpenseCreate, ExpenseOut
from src.dependencies import db_dependency, user_dependency
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from .models import Expense
from datetime import datetime
from sqlalchemy import select

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def list_expenses(
    user=Depends(user_dependency),
    db=Depends(db_dependency)
):
    
    query = select(Expense).where(Expense.user_id == user.id)
    result = await db.execute(query)
    expenses = result.scalars().all()

    print(expenses)

    return [e.as_dict() for e in expenses]


@router.post("/", response_model=ExpenseOut)
async def create_expense(
    expense_in: ExpenseCreate, 
    user=Depends(user_dependency),
    db=Depends(db_dependency)
):
    new_expense = Expense(
        user_id=user.id,
        category_id=expense_in.category,
        amount=expense_in.amount,
        description=expense_in.description,
        spent_at=datetime.now()
    )

    await db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)

    return new_expense
