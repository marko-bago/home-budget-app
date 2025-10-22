from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class ExpenseCreate(BaseModel):

    category: str = Field(
        title="Category Name",
        max_length=50
    )
    amount: float = Field(
        title="Amount",
        description="The amount of money allocated to this expense.",
        gt=0
    )
    description: str = Field(
        title="Description",
        description="A brief description of the expense.",
        max_length=200,
        default=None
    )
    created_at: datetime = Field(
        title="Created at",
        description="Date and time when expense was created.",
        default=None
    )


class ExpenseOut(BaseModel):
    id: int
    amount: float
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True