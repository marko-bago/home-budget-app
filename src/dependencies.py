from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionFactory

from fastapi.security import OAuth2PasswordBearer
import jwt
from fastapi import Depends, Security, HTTPException, status
from src.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.auth.security_utils import ALGORITHM
from typing import Annotated

async def get_session():
    db = SessionFactory()
    try:
        yield db
    finally:
        await db.close()

db_dependency = Annotated[AsyncSession, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"api/{settings.VERSION}/auth/login")

async def get_current_user(token: str = Security(oauth2_scheme), db: AsyncSession = db_dependency):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

user_dependency = Annotated[User , Depends(get_current_user)]

async def get_current_active_superuser(current_user: user_dependency) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user

