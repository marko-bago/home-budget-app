from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base

class Expense(Base):

    """Represents a single financial expense made by a user."""

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    spent_at = Column(DateTime(timezone=True), server_default=func.now())
    date = Column(DateTime, nullable=False)

