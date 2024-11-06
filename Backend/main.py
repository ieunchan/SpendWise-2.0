from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date
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

class Userdata(Base):
    __tablename__ = "userdata"
    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String, index=True)   # 지출 또는 수입
    description = Column(String, index=True)        # 내역 (식비, 교통비, 쇼핑, 기타 등)
    description_detail = Column(String, nullable=True)  # 기타일 경우 설명 추가 (nullable)
    amount = Column(Integer, index=True)            # 금액
    date = Column(Date, index=True)  

Base.metadata.create_all(bind=engine) # 데이터베이스 테이블 생성

class UserdataCreate(BaseModel):
    transaction_type: str
    description: str
    description_detail: Optional[str] = None  # 선택적 필드로 설정
    amount: int
    date: date

class UserdataResponse(BaseModel):
    id: int
    transaction_type: str
    description: str
    description_detail: Optional[str] = None
    amount: int
    date: date

    class Config:
        orm_mode = True

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
    db_userdata = Userdata(**userdata.dict())
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

# 지출 데이터 조회 API (금액만 반환)
@app.get("/userdata/expense/", response_model=List[dict])
def read_user_expense_amount(db: Session = Depends(get_db)):
    expense_amount = db.query(Userdata.amount).filter(Userdata.transaction_type == "지출").all()
    expense_datas = [{"amount": amount[0]} for amount in expense_amount]
    return expense_datas

# 수입 데이터 조회 API (금액만 반환)
@app.get("/userdata/income/", response_model=List[dict])
def read_user_income_amount(db: Session = Depends(get_db)):
    income_amount = db.query(Userdata.amount).filter(Userdata.transaction_type == "수입").all()
    income_datas = [{"amount": amount[0]} for amount in income_amount]
    return income_datas

