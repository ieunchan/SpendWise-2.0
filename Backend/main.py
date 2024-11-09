from sqlalchemy import create_engine, Column, Integer, String, Date, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import FastAPI, Query, Depends,HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from decouple import AutoConfig
import matplotlib.pyplot as plt
from pydantic import BaseModel
from datetime import datetime
from datetime import date
import pandas as pd


config = AutoConfig()

DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
Base = declarative_base()

app = FastAPI()

# 유저 데이터 모델 생성(테이블 생성)
class Userdata(Base):
    __tablename__ = "userdata"
    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String, index=True)   # 지출 또는 수입
    description = Column(String, index=True)        # 내역 (식비, 교통비, 쇼핑, 기타 등)
    description_detail = Column(String, nullable=True)  # 기타일 경우 설명 추가 (nullable)
    amount = Column(Integer, index=True)            # 금액
    date = Column(Date, index=True)  

Base.metadata.create_all(bind=engine) # 데이터베이스 테이블 생성

# 입력받은 유저 데이터의 유효성을 검사하는 모델
class UserdataCreate(BaseModel):
    transaction_type: str
    description: str
    description_detail: Optional[str] = None  # 선택적 필드로 설정
    amount: int
    date: date

# 리턴하는 데이터의 유효성을 검사하는 모델
class UserdataResponse(BaseModel):
    id: int
    transaction_type: str
    description: str
    description_detail: Optional[str] = None
    amount: int
    date: date

    # sqlalchemy 모델을 json으로 자동으로 변환
    class Config:
        orm_mode = True

# 지출 내역의 총액 순위의 기본모델
class ExpenseSummary(BaseModel):
    description: str
    total_amount: int

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 연도와 월을 받아 해당 월의 시작일과 종료일을 반환하는 함수
def get_month_range(year: int, month: int):
    start_of_month = datetime(year, month, 1)
    if month == 12:
        end_of_month = datetime(year + 1, 1, 1)
    else:
        end_of_month = datetime(year, month + 1, 1)
    return start_of_month, end_of_month

# 데이터 생성 API
@app.post("/userdata/", response_model=UserdataResponse)
def create_userdata(userdata: UserdataCreate, db: Session = Depends(get_db)):
    db_userdata = Userdata(**userdata.model_dump())
    db.add(db_userdata)
    db.commit()
    db.refresh(db_userdata)
    return db_userdata

# 지출 데이터 조회 API (총 금액만 반환)
@app.get("/userdata/expense/", response_model=List[dict])
def read_user_expense_amount(
    year: int = Query(..., description="조회할 년도"),
    month: int = Query(..., description="조회할 월"),
    db: Session = Depends(get_db)
    ):

    try:
        start_of_month, end_of_month = get_month_range(year,month)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 연도 또는 월입니다.")
    
    # 해당 월의 지출 데이터 필터링
    expense_amount = (
        db.query(Userdata.amount)
        .filter(Userdata.transaction_type == "지출")
        .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
        .all()
    )

    # 결과를 딕셔너리로 변환하여 반환
    expense_datas = [{"amount": amount[0]} for amount in expense_amount]
    return expense_datas

# 수입 데이터 조회 API (총 금액만 반환)
@app.get("/userdata/income/", response_model=List[dict])
def read_user_income_amount(
    year: int = Query(...,description="조회할 년도"),
    month: int = Query(..., description="조회할 월"),
    db: Session = Depends(get_db)
    ):
    
    try:
        start_of_month, end_of_month = get_month_range(year, month)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 연도 또는 월입니다.")

    # 해당 월의 수입 데이터만 필터링
    income_amount = (
        db.query(Userdata.amount)
        .filter(Userdata.transaction_type == "수입")
        .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
        .all()
    )

    # 결과를 딕셔너리로 변환하여 반환
    income_datas = [{"amount": amount[0]} for amount in income_amount]
    return income_datas

# 지출 금액의 순위 조회 API
@app.get("/userdata/expense/ranking/", response_model=List[dict])
def expense_ranking(
    year: int = Query(..., description="조회할 연도"),
    month: int = Query(..., description="조회할 월"),
    db: Session = Depends(get_db)
):
    start_of_month, end_of_month = get_month_range(year, month)

    try:
        # 해당 월의 지출 금액을 description 별로 합산하여 순위 조회
        expense_rank = (
            db.query(Userdata.description, func.sum(Userdata.amount).label("total_amount"))
            .filter(Userdata.transaction_type == "지출")
            .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
            .group_by(Userdata.description)
            .order_by(func.sum(Userdata.amount).desc())
            .all()
        )

    except SQLAlchemyError as e:
        # SQLAlchemy 오류 발생 시 예외 처리 및 로그 출력
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="지출 랭킹 데이터베이스 쿼리 중 오류가 발생했습니다.")

    # 결과가 비어 있는 경우 예외 처리
    if not expense_rank:
        return [{"description": "데이터 없음", "total_amount": 0}]
    
    # 안전한 데이터 접근
    expense_rank_data = [
        {
            "description": item[0] if len(item) > 0 else "데이터 없음",
            "total_amount": item[1] if len(item) > 1 else 0
        }
        for item in expense_rank
    ]
    return expense_rank_data

# 지출 항목별 상세 내역 조회 API
@app.get("/userdata/expense/details/", response_model=List[dict])
def get_expense_details(
    description: str = Query(..., description="지출 항목 이름"),
    db: Session = Depends(get_db)
):
    # 특정 description의 상세 내역 조회
    expense_details = db.query(Userdata).filter(Userdata.description == description).all()
    
    # 결과를 딕셔너리 형태로 반환
    details = [
        {
            "날짜": detail.date,
            "항목": detail.description,
            "금액": detail.amount
        }
        for detail in expense_details
    ]
    return details