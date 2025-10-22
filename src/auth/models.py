from src.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, Boolean, String, DateTime, func

class User(Base):
    
    """Represents a regular app user."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    balance = Column(Float, default=1000.0)  # predefined starting balance
    created_at = Column(DateTime(timezone=True), server_default=func.now())
