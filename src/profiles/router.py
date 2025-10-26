from fastapi import APIRouter, status, Depends, HTTPException
from src.dependencies import get_session, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from sqlalchemy import select, update
from src.auth.schemas import UserOut

router = APIRouter()

@router.get("/", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user_info(
    user: User = Depends(get_current_user)
):
    return user

@router.delete("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def remove_profile(
    user_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()

    return user



