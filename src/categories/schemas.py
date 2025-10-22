from pydantic import BaseModel, Field
from datetime import datetime

class CategoryCreate(BaseModel):
    
    name: str = Field(
        title="Name",
        description="Name of category.",
        max_length=50,
        default="Other"
    )
    description: str = Field(
        title="Description",
        description="A brief description of category.",
        max_length=200,
        default="Everything else."
    )
    created_at: datetime = Field(
        title="Created at",
        description="Date and time when category was created.",
        default=None
    )