from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from src.categories.schemas import CategoryOut

class TransactionCreate(BaseModel):
    category: str 
    amount: float = Field(title="amount", gt=0, description="Amount must be greater than 0")
    description: Optional[str] = None
    type: str

class TransactionUpdate(BaseModel):
    category_new: str
    description_new: Optional[str] = None

class TransactionOut(BaseModel):
    id: int
    amount: float
    description: Optional[str] = None
    created_at: datetime
    category: Optional[CategoryOut] 

    model_config = ConfigDict(from_attributes=True)