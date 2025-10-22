from fastapi import APIRouter, status

from .schemas import UserCreate, UserResponse, LoginRequest, Token
from .models import User
from src.dependencies import db_dependency
from fastapi import HTTPException
from .security_utils import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy import select
from datetime import timedelta
from typing import Annotated

router = APIRouter()

@router.post("/register", response_model=None)
async def register(user_in: UserCreate, db: db_dependency):

    query_check_email = select(User).where(User.email == user_in.email)
    check_email = await db.execute(query_check_email)

    query_check_usrname = select(User).where(User.username == user_in.username)
    check_username = await db.execute(query_check_usrname)

    if check_email.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    if check_username.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken.")

    # Create user
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        balance=1000.0  # default balance
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": f"User '{new_user.username}' successfully registered"}


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    
    print(f"Form data: {form_data}")

    query_login = select(User).where(User.username == form_data.username)
    result = await db.execute(query_login)
    user = result.scalars().first()

    print(user)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.username}, expires_delta=timedelta(minutes=30))

    return Token(access_token=token)