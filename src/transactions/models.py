from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base
from enum import Enum

class TransactionType(Enum):
    income = "income"
    expense = "expense"


class Transaction(Base):

    """Represents a single financial expense made by a user."""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(Integer, ForeignKey("categories.name", ondelete="SET NULL"))
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    type = Column(
        Enum(TransactionType, name="transaction_type"), 
        nullable=False,
        default=TransactionType.expense
    )
    spent_at = Column(DateTime(timezone=True), server_default=func.now())

