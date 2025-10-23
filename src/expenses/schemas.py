from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ExpenseCreate(BaseModel):
    category: str 
    amount: float 
    description: Optional[str] = None
    spent_at: datetime 

class ExpenseUpdate(BaseModel):
    category_new: str
    amount_new: float
    description: Optional[str] = None

class ExpenseOut(BaseModel):
    id: int
    amount: float
    description: Optional[str] = None
    spent_at: datetime

    class Config:
        from_attributes = True