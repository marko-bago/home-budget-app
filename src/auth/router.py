from fastapi import APIRouter, status

from .schemas import UserCreate, UserResponse, LoginRequest, Token
from .models import User
from src.dependencies import db_dependency
from fastapi import HTTPException
from .security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: db_dependency):

    check_email = db.query(User).filter(User.email == user_in.email).first()
    check_username = db.query(User).filter(User.username == user_in.username).first()

    if check_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    if check_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken.")

    # Create user
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        balance=1000.0  # default balance
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(user_id=new_user.id, message=f"User '{new_user.username}' successfully registered")


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: db_dependency):

    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return Token(access_token=token)