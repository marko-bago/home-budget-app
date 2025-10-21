from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

class ExpenseCreate(BaseModel):
    category_id: str = Field(
        title="Category id",
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

class ExpenseCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

