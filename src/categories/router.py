from fastapi import APIRouter, Depends
from .schemas import CategoryCreate
from src.dependencies import db_dependency, user_dependency
from .models import Category

router = APIRouter()

@router.post("/", response_model=None)
async def create_category(
    category_in: CategoryCreate, 
    user=Depends(user_dependency),
    db=Depends(db_dependency),
):
    new_category = Category(
        user_id = user.id,
        name = category_in.name,
        description = category_in.description
    )

    await db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return {"message": f"Category ${new_category.name} added."}
