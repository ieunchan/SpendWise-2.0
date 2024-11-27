from fastapi import FastAPI
from app.routes import expense, income, others

# 각 라우터의 앱을 실행하는 main 앱입니다.

# FastAPI 인스턴스 생성
app = FastAPI()

# 라우터 등록
app.include_router(expense.router, prefix="/userdata/expense", tags=["Expense"])
app.include_router(income.router, prefix="/userdata/income", tags=["Income"])
app.include_router(others.router, prefix="/userdata", tags=["Others"])