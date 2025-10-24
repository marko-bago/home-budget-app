from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TransactionCreate(BaseModel):
    category: str 
    amount: float 
    description: Optional[str] = None
    type: str
    spent_at: datetime 

class TransactionUpdate(BaseModel):
    category_new: str
    amount_new: float
    description: Optional[str] = None

class TransactionOut(BaseModel):
    id: int
    amount: float
    description: Optional[str] = None
    spent_at: datetime

    class Config:
        from_attributes = True