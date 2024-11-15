from sqlalchemy import create_engine, Column, Integer, String, Date, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import FastAPI, Query, Depends,HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from decouple import AutoConfig
from sqlalchemy.sql import and_
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
    transaction_type = Column(String, index=True)   # 지출 또는 소득
    description = Column(String, index=True)        # 내역 (식비, 교통비, 쇼핑, 기타 등)
    description_detail = Column(String, nullable=True)  # 기타일 경우 설명 추가 (nullable)
    amount = Column(Integer, index=True)            # 금액
    date = Column(Date, index=True)  

Base.metadata.create_all(bind=engine) # 데이터베이스 테이블 생성

# 입력받은 유저 데이터의 유효성을 검사하는 모델
class UserdataCreate(BaseModel):
    transaction_type: str
    description: str
    description_detail: Optional[str] = None 
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
def get_month_range(year: int, month: int, day: Optional[int] = None):
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

# 소득 데이터 조회 API (총 금액만 반환)
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

    # 해당 월의 소득 데이터만 필터링
    income_amount = (
        db.query(Userdata.amount)
        .filter(Userdata.transaction_type == "소득")
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
    year: int = Query(..., description="조회할 년도"),
    month: int = Query(..., description="조회할 월"),
    description: str = Query(..., description="지출 항목 이름"),
    db: Session = Depends(get_db)
):
    
    start_of_month, end_of_month = get_month_range(year, month)

    # 특정 description의 상세 내역 조회
    expense_details = (
        db.query(Userdata)
        .filter(Userdata.description == description)
        .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
        .all())
    
    # 결과를 딕셔너리 형태로 반환
    details = [
        {
            "날짜": detail.date,
            "내역": detail.description,
            "상세내역": detail.description_detail,
            "금액": detail.amount
        }
        for detail in expense_details
    ]
    return details


@app.get("/userdata/income/ranking/", response_model=List[dict])
def income_ranking(
    year: int = Query(..., description="조회할 년도"),
    month: int = Query(..., description="조회할 월"),
    db: Session = Depends(get_db)
):
    start_of_month, end_of_month = get_month_range(year, month)

    try:
        income_rank = (
            db.query(Userdata)
            .filter(Userdata.transaction_type == "소득")
            .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
            .order_by(Userdata.date.desc())
            .all()
            )
    except SQLAlchemyError as e:
        # SQLAlchemy 오류 발생 시 예외 처리 및 로그 출력
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="소득 랭킹 데이터베이스 쿼리 중 오류가 발생했습니다.")
    
    if not income_rank:
        return [{"날짜": "데이터 없음", "내역": "내역 없음", "금액": 0}]
    
    income_rank_data = [
        {
        "날짜": income.date.strftime("%Y-%m-%d"),  # 날짜를 "YYYY-MM-DD" 형식으로 변환
        "내역": income.description,
        "금액": income.amount  
        }
    for income in income_rank
    ]
    return income_rank_data

# 총 자산, 총 소득, 총 지출을 표시하는 API
# @app.get("/userdata/total_asset/", response_model=List[dict])
# def get_total_assets(db: Session = Depends(get_db)):
#     def get_total_by_type(transaction_type: str, year: int):
#         try:
#             # 트랜잭션 유형에 따라 합계를 계산
#             result = (
#                 db.query(func.sum(Userdata.amount).label("total_amount"))
#                 .filter(Userdata.transaction_type == transaction_type)
#                 .filter(func.extract('year', Userdata.date) == year)
#                 .scalar()  # 합계 값을 직접 가져오기
#             )
#             return result or 0  # None일 경우 0 반환
#         except SQLAlchemyError as e:
#             print(f"SQLAlchemy Error: {str(e)}")
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"{transaction_type} 총액 데이터베이스 쿼리 중 오류가 발생했습니다."
#             )

#     # 소득과 지출의 합계 계산
#     total_income = get_total_by_type("소득")
#     total_expend = get_total_by_type("지출")

#     # 총 자산 계산
#     total_assets = total_income - total_expend

#     return [{"총 자산": total_assets, "총 소득": total_income, "총 지출": total_expend}]

# 년간 지출 합계를 반환하는 API
@app.get("/userdata/expense/annual", response_model=List[ExpenseSummary])
def get_annual_expense_by_description(
    year: int = Query(..., description="조회할 연도"),
    transaction_type: str = Query(..., description="년도 별 지출"),
    db: Session = Depends(get_db)
):
    try:
        # 연도별 소득 또는 지출 합계를 description별로 합산하여 조회
        annual_expense = (
            db.query(Userdata.description, func.sum(Userdata.amount).label("total_amount"))
            .filter(
                and_(
                    Userdata.transaction_type == transaction_type,  # 거래 유형 필터
                    func.extract('year', Userdata.date) == year  # 연도 필터링
                )
            )
            .group_by(Userdata.description)
            .order_by(func.sum(Userdata.amount).desc())  # 금액 순으로 정렬
            .all()
        )

        # 결과가 비어 있을 경우 기본 값 반환
        if not annual_expense:
            return [{"description": "데이터 없음", "total_amount": 0}]
        
        # Pydantic 모델 형식에 맞게 데이터 변환
        annual_expense_data = [
            ExpenseSummary(description=item[0], total_amount=item[1])
            for item in annual_expense
        ]
        
        return annual_expense_data

    except SQLAlchemyError as e:
        # SQLAlchemy 오류 발생 시 예외 처리 및 로그 출력
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="연도별 데이터베이스 쿼리 중 오류가 발생했습니다.")




# 년간 소득 합계를 반환하는 API
@app.get("/userdata/income/annual", response_model = List[dict])
def get_annual_income(
    year: int = Query(..., description="조회할 년도"),
    transaction_type: str = Query(..., description="년도 별 소득"),
    db: Session = Depends(get_db)
):
    try:
        annual_income = {
            db.query(func.sum(Userdata.amount).label("total_amount"))
            .filter(Userdata.transaction_type == transaction_type)
            .filter(func.extract('year', Userdata.date) == year)
            .scalar()
        }

        # 소득이 없을 경우 0 반환
        if not annual_income:
            return [{"year": year, "total_amount": 0}]
        
        # 소득 데이터 반환
        return [{"year": year, "total_amount": annual_income}]

    except SQLAlchemyError as e:
        # SQLAlchemy 오류 발생 시 예외 처리 및 로그 출력
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="연도별 데이터베이스 쿼리 중 오류가 발생했습니다.")
