from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

class UserOut(BaseModel):
    id: str
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
