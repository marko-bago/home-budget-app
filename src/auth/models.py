from src.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, Boolean, String, DateTime, func

class User(Base):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    balance = Column(Float, default=1000.0) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship("Transaction", 
                                back_populates="user", 
                                cascade="all, delete-orphan")

    categories = relationship("Category", 
                              back_populates="user",
                              cascade="all, delete-orphan")