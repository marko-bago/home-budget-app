from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base

class Expense(Base):

    """Represents a single financial expense made by a user."""

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("expense_categories.id", ondelete="SET NULL"))
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    spent_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    category = relationship("ExpenseCategory", back_populates="expenses")
    user = relationship("User", back_populates="expenses")


class ExpenseCategory(Base):

    """Represents a single expense category."""

    __tablename__ = "expense_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

    # Relationship: one category has many expenses
    expenses = relationship(
        "Expense",
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )