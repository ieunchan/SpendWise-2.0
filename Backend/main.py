from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, List
from datetime import date
from decouple import AutoConfig

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

# 데이터 생성 API
@app.post("/userdata/", response_model=UserdataResponse)
def create_userdata(userdata: UserdataCreate, db: Session = Depends(get_db)):
    db_userdata = Userdata(**userdata.model_dump())
    db.add(db_userdata)
    db.commit()
    db.refresh(db_userdata)
    return db_userdata

# 지출 및 수입 데이터 조회 API (특정 타입만 필터링 가능)
@app.get("/userdata/all_type/", response_model=List[UserdataResponse])
def read_userdata_by_type(transaction_type: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Userdata)
    if transaction_type:
        query = query.filter(Userdata.transaction_type == transaction_type)
    else:
        query = query.filter(Userdata.transaction_type.in_(["지출", "수입"]))
    userdatas = query.all()
    return userdatas

# 지출 데이터 조회 API (총 금액만 반환)
@app.get("/userdata/expense/", response_model=List[dict])
def read_user_expense_amount(db: Session = Depends(get_db)):
    expense_amount = db.query(Userdata.amount).filter(Userdata.transaction_type == "지출").all()
    expense_datas = [{"amount": amount[0]} for amount in expense_amount]
    return expense_datas

# 수입 데이터 조회 API (총 금액만 반환)
@app.get("/userdata/income/", response_model=List[dict])
def read_user_income_amount(db: Session = Depends(get_db)):
    income_amount = db.query(Userdata.amount).filter(Userdata.transaction_type == "수입").all()
    income_datas = [{"amount": amount[0]} for amount in income_amount]
    return income_datas

# 지출 금액의 순위 조회 API
@app.get("/userdata/expense/ranking/", response_model=List[ExpenseSummary])
def expense_ranking(db: Session = Depends(get_db)):
    expense_rank = (db.query(Userdata.description, func.sum(Userdata.amount).label("total_amount"))
                    .filter(Userdata.transaction_type == "지출")
                    .group_by(Userdata.description)
                    .all())
    return expense_rank


