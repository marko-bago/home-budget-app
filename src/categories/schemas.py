from pydantic import BaseModel, Field, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)