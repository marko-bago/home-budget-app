from fastapi import APIRouter, status, Depends, HTTPException
from .schemas import ExpenseCreate, ExpenseOut, ExpenseUpdate
from src.dependencies import get_session, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.categories.models import Category
from .models import Expense
from datetime import datetime
from sqlalchemy import select, update

router = APIRouter()

@router.get("/", response_model=list[ExpenseOut], status_code=status.HTTP_200_OK)
async def list_expenses(
    user=Depends(get_current_user),
    db=Depends(get_session)
):
    
    query = select(Expense).where(Expense.user_id == user.id)
    result = await db.execute(query)
    expenses = result.scalars().all()

    return expenses


@router.post("/", response_model=ExpenseOut)
async def create_expense(
    expense_in: ExpenseCreate, 
    user=Depends(get_current_user),
    db=Depends(get_session)
):
    if user.balance < expense_in.amount:
        raise HTTPException(status_code=409, detail="Insufficient balance.")

    # Try to deduct the balance atomically to avoid clashes
    query = (
        update(User)
        .where(User.id == user.id, User.balance >= expense_in.amount)
        .values(balance=User.balance - expense_in.amount)
        .returning(User.id)
    )

    updated_user = (await db.execute(query)).scalar()

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user."
        )

    new_expense = Expense(
        user_id=user.id,
        category_id=expense_in.category,
        amount=expense_in.amount,
        description=expense_in.description,
        spent_at=datetime.now()
    )
    
    db.add(new_expense)

    await db.commit()
    await db.refresh(new_expense)

    return new_expense

@router.put("/{expense_id}", response_model=ExpenseOut)
async def create_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    user=Depends(get_current_user),
    db=Depends(get_session)
):  
    query_check_exists = select(Expense).where(Expense.id == expense_id)
    expense = (await db.execute(query_check_exists)).scalars().first()

    query_check_exists = select(Category).where(expense_update.category == Category.name)
    category = (await db.execute(query_check_exists)).scalars().first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found.")

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

    # Ensure the user owns this expense
    if expense.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this category.")

    diff = expense_update.amount - expense.amount

    # If increasing the expense, check balance first
    if diff > 0 and user.balance < diff:
        raise HTTPException(status_code=409, detail="Insufficient balance.")

    # Try to deduct the balance atomically to avoid clashes
    query = (
        update(User)
        .where(User.id == user.id, User.balance >= diff)
        .values(balance=User.balance - diff)
        .returning(User.id)
    )

    updated_user = (await db.execute(query)).scalar()

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user."
        )
    
    expense.category = expense_update.category_new
    expense.amount = expense_update.amount_new
    expense.description = expense_update.description

    db.add(expense)
    await db.commit()
    await db.refresh(expense)

    return expense

@router.delete("/{expense_id}", response_model=None)
async def delete_category(
    expense_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    
    query_check_exists = select(Expense).where(Expense.id == expense_id)
    expense = (await db.execute(query_check_exists)).scalars().first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found.")

    # Ensure the user owns this expense
    if expense.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this category.")


    # Try to increase the balance atomically to avoid clashes
    query = (
        update(User)
        .where(User.id == user.id)
        .values(balance=User.balance + expense.amount)
        .returning(User.id)
    )

    updated_user = (await db.execute(query)).scalar()

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user."
        )
    
    await db.delete(expense)
    await db.commit()

    return {"message": f"Expense '{expense.id}' deleted successfully."}
