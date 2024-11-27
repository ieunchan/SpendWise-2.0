from pydantic import BaseModel
from typing import Optional
from datetime import date

# pydantic 모델을 사용하여 요청 및 응답 데이터를 검증합니다.

class UserdataCreate(BaseModel):
    transaction_type: str
    description: str
    description_detail: Optional[str] = None
    amount: int
    date: date

class UserdataResponse(UserdataCreate):
    id: int

    class Config:
        orm_mode = True

class ExpenseSummary(BaseModel):
    description: str
    total_amount: int