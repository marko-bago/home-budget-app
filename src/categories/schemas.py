from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CategoryCreate(BaseModel):
    name: str 
    description: str 

class CategoryUpdate(BaseModel):
    name_new: str
    description: Optional[str] = None

class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True