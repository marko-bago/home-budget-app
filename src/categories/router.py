from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from .schemas import CategoryCreate, CategoryUpdate, CategoryOut
from src.auth.models import User
from src.dependencies import get_session, get_current_user
from .models import Category
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/", response_model=list[CategoryOut])
async def get_categories(
    user=Depends(get_current_user),
    db=Depends(get_session)
):
    query = select(Category).where(Category.user_id == user.id)
    result = await db.execute(query)
    categories = result.scalars().all()

    return categories


@router.post("/", response_model=CategoryOut)
async def create_category(
    category_in: CategoryCreate, 
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    query_check_exists = select(Category).where(Category.name == category_in.name)
    check_exists = await db.execute(query_check_exists)

    if check_exists.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with same name already exists.")

    new_category = Category(
        user_id = user.id,
        name = category_in.name,
        description = category_in.description
    )

    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate, 
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    
    query_check_exists = select(Category).where(Category.id == category_id)
    category = (await db.execute(query_check_exists)).scalars().first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

    # Ensure the user owns this category
    if category.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this category.")

    query_check_name = select(Category).where(Category.name == category_update.name_new, Category.id != category_id)
    name_result = await db.execute(query_check_name)
    if name_result.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Another category with this name already exists.")

    # Update fields
    category.name = category_update.name_new
    category.description = category_update.description

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category

@router.delete("/{category_id}", response_model=None)
async def delete_category(
    category_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    
    query_check_exists = select(Category).where(Category.id == category_id)
    category = (await db.execute(query_check_exists)).scalars().first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

    # Ensure the user owns this category
    if category.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this category.")

    await db.delete(category)
    await db.commit()

    return {"message": f"Category '{category.name}' deleted successfully."}