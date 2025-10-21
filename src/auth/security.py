from datetime import datetime, timedelta
from pydantic import SecretStr
import jwt

from passlib.context import CryptContext
from src.config import settings


ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: SecretStr):
    return pwd_context.hash(password.get_secret_value())

def verify_password(plain_password: SecretStr, hashed_password: str):
    return pwd_context.verify(plain_password.get_secret_value(), hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return token

