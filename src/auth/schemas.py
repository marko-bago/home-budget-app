from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(UserBase):
    username: str
    email: str

class UserResponse(BaseModel):
    user_id: str
    message: str


class LoginRequest(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
