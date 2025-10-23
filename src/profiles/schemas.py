from datetime import datetime
from pydantic import BaseModel

class BalanceIn(BaseModel):
    amount: float

class BalanceOut(BaseModel):
    balance: float