from fastapi import APIRouter, status, Depends, HTTPException
from .schemas import TransactionCreate, TransactionOut, TransactionUpdate
from src.dependencies import get_session, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.auth.models import User
from src.categories.models import Category
from .models import Transaction, TransactionType
from datetime import datetime, date, timedelta, time
from sqlalchemy import select, update, func, case
from fastapi import Query
from dateutil.relativedelta import relativedelta

router = APIRouter()

@router.get("/", response_model=list[TransactionOut], status_code=status.HTTP_200_OK)
async def list_transactions(
    category: str = Query(None, description="Filter by category"),
    amount_min: float = Query(None, ge=0),
    amount_max: float = Query(None, ge=0),
    from_date: date = Query(None, description="Filter transactions from this date"),
    to_date: date = Query(None, description="Filter transactions to this date"),
    period: str = Query(None, description="Filter transactions by predefined period"),
    sort_by: str = Query("created_at", pattern="^(amount|created_at)$", description="Sort by 'amount' or 'created_at'"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order: 'asc' or 'desc'"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):  
    
    query = select(Transaction).options(joinedload(Transaction.category)).where(Transaction.user_id == user.id)

    if category:
        query_check_exists = select(Category).where(category == Category.name)
        cat_db = (await db.execute(query_check_exists)).scalars().first()
        if not cat_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
        query = query.where(Transaction.category_id == cat_db.id)

    if amount_min:
        query = query.where(Transaction.amount >= amount_min)

    if amount_max:
        query = query.where(Transaction.amount <= amount_max)

    # period will override form_date and to_date parameters
    if period:
        period_map = {
            "week": relativedelta(weeks=1),
            "month": relativedelta(months=1),
            "quarter": relativedelta(months=3),
            "year": relativedelta(years=1)
        }
        period = period.lower()
        if period in period_map:
            from_date = datetime.now().date() - period_map[period]
            to_date = datetime.now().date()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid 'period' value. Accepted values are 'week', 'month', '3months'.")

    if from_date:
        from_date = datetime.combine(from_date, time.min)
        query = query.where(Transaction.created_at >= from_date)

    if to_date:
        to_date = datetime.combine(to_date, time.max)
        query = query.where(Transaction.created_at <= to_date)
    
    order_column = Transaction.created_at if sort_by == "date" else Transaction.amount
    if sort_order == "desc":
        query = query.order_by(order_column.desc())
    else:
        query = query.order_by(order_column.asc())

    result = await db.execute(query)
    transactions = result.scalars().all()

    return transactions

@router.get("/summary", status_code=status.HTTP_200_OK)
async def get_summary(
    category: str = Query(None, description="Filter by category"),
    amount_min: float = Query(None, ge=0),
    amount_max: float = Query(None, ge=0),
    from_date: date = Query(None, description="Filter transactions from this date"),
    to_date: date = Query(None, description="Filter transactions to this date"),
    period: str = Query(None, description="Filter transactions by predefined period"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):  
    
    adjusted_amount = case(
        (Transaction.type == TransactionType.expense, -Transaction.amount),
        else_=Transaction.amount
    )
    query = select(
        func.count(Transaction.id),
        func.sum(adjusted_amount),
        func.avg(adjusted_amount)
    ).where(Transaction.user_id == user.id)

    if category:
        query_check_exists = select(Category).where(category == Category.name)
        cat_db = (await db.execute(query_check_exists)).scalars().first()
        if not cat_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
        query = query.where(Transaction.category_id == cat_db.id)

    if amount_min:
        query = query.where(Transaction.amount >= amount_min)

    if amount_max:
        query = query.where(Transaction.amount <= amount_max)

    if period:
        period_map = {
            "week": timedelta(days=7),
            "month": timedelta(days=30),
            "quarter": timedelta(days=90),
            "year": timedelta(days=365)
        }
        period = period.lower()
        if period in period_map:
            from_date = datetime.now()- period_map[period]
            to_date = datetime.now()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid 'period' value. Accepted values are 'week', 'month', '3months'.")

    if from_date:
        from_date = datetime.combine(from_date, time.min)
        query = query.where(Transaction.created_at >= from_date)

    if to_date:
        to_date = datetime.combine(to_date, time.max)
        query = query.where(Transaction.created_at <= to_date)
    

    result = await db.execute(query)

    count, total, avg = result.first()
    return {"num_of_transactions": count, "sum_of_transactions": total , "avg_transaction_amount": avg}

@router.post("/", response_model=TransactionOut)
async def create_transaction(
    transaction_in: TransactionCreate, 
    user=Depends(get_current_user),
    db=Depends(get_session)
):
    query_check_exists = select(Category).where(transaction_in.category == Category.name)
    cat_db = (await db.execute(query_check_exists)).scalars().first()

    if not cat_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

    if transaction_in.type == TransactionType.expense and user.balance < transaction_in.amount:
        raise HTTPException(status_code=409, detail="Insufficient balance.")

    if transaction_in.type == TransactionType.expense:
    # If it's an expense, the amount must be negative for the balance update
        balance_change = -transaction_in.amount
    elif transaction_in.type == TransactionType.income:
        # If it's income, the amount is positive
        balance_change = transaction_in.amount

    # Try to deduct the balance atomically to avoid clashes
    query = (
        update(User)
        .where(User.id == user.id)
        .values(balance=User.balance + balance_change)
        .returning(User.id)
    )

    updated_user = (await db.execute(query)).scalar()

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user."
        )

    new_trans = Transaction(
        user_id=user.id,
        category=cat_db,
        amount=transaction_in.amount,
        description=transaction_in.description,
        type=transaction_in.type
    )
    
    db.add(new_trans)

    await db.commit()
    await db.refresh(new_trans)

    return new_trans

@router.put("/{transaction_id}", response_model=TransactionOut)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    user=Depends(get_current_user),
    db=Depends(get_session)
):  
    query_check_exists = select(Transaction).options(joinedload(Transaction.category)).where(Transaction.id == transaction_id)
    transaction = (await db.execute(query_check_exists)).scalars().first()

    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")

    query_check_exists = select(Category).where(transaction_update.category_new == Category.name)
    cat_db = (await db.execute(query_check_exists)).scalars().first()

    if not cat_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

    # Ensure the user owns this transaction
    if transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this category.")

    diff = transaction_update.amount_new - transaction.amount

    if transaction.type == TransactionType.expense:
            # For expense, increasing amount deducts from balance
        if diff > 0 and user.balance < diff:
            raise HTTPException(status_code=409, detail="Insufficient balance.")

        query = (
            update(User)
            .where(User.id == user.id, User.balance >= diff)
            .values(balance=User.balance - diff)
            .returning(User.id)
        )
    elif transaction.type == TransactionType.income:
        # For income, decreasing amount reduces user's balance
        if diff < 0 and user.balance < -diff:
            raise HTTPException(status_code=409, detail="Insufficient balance to reduce income.")

        query = (
            update(User)
            .where(User.id == user.id)
            .values(balance=User.balance + diff)
            .returning(User.id)
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type.")

    updated_user = (await db.execute(query)).scalar()

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user."
        )
    
    transaction.category_id = cat_db.id
    transaction.amount = transaction_update.amount_new
    transaction.description = transaction_update.description

    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)

    return transaction

@router.delete("/{transaction_id}", response_model=None)
async def delete_transaction(
    transaction_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    
    query_check_exists = select(Transaction).where(Transaction.id == transaction_id)
    transaction = (await db.execute(query_check_exists)).scalars().first()

    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")

    if transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this category.")

    if transaction.type == TransactionType.expense:
        query = (
            update(User)
            .where(User.id == user.id)
            .values(balance=User.balance + transaction.amount)
            .returning(User.id)
        )
    elif transaction.type == TransactionType.income:
        query = (
            update(User)
            .where(User.id == user.id)
            .values(balance=User.balance - transaction.amount)
            .returning(User.id)
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type.")

    updated_user = (await db.execute(query)).scalar()

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user."
        )
    
    await db.delete(transaction)
    await db.commit()

    return {"message": f"Transaction '{transaction.id}' deleted successfully."}
