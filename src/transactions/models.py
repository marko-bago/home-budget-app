from enum import Enum
from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import relationship
from src.database import Base

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class Transaction(Base):
    """Represents a single financial transaction made by a user."""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    
    # Enum column for transaction type
    type = Column(
        SQLEnum(TransactionType, name="transaction_type", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TransactionType.expense
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions", lazy="joined")
