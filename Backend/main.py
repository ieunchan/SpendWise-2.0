from fastapi import FastAPI, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
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
    id = Column(Integer, primary_key=True, index=True) # 추가한 유저
    transaction_type = Column(String, index=True) # 지출 or 수입인지 분류
    description = Column(String, index=True) # 지출 형식을 분류
    amount = Column(Integer, index=True) # 지출액 or 수입액
    date = Column(Date, index=True) # 지출 or 수입 날짜

Base.metadata.create_all(bind=engine) # 데이터베이스 테이블 생성

class UserdataCreate(BaseModel):
    transaction_type: str
    description: str
    amount: int
    date: date

# 입력받은 유저 데이터를 DB에 저장하는 API
@app.post("/userdata/")
def create_userdata(userdata: UserdataCreate):
    db = SessionLocal()
    db_userdata = Userdata(
        transaction_type = userdata.transaction_type,
        description = userdata.description,
        amount = userdata.amount,
        date = userdata.date)
    db.add(db_userdata)
    db.commit()
    db.refresh(db_userdata)
    db.close()
    return db_userdata

@app.get("/userdata/all_type")
def read_user_expense_income_amount():
    db = SessionLocal()
    # transaction_type이 '지출'인 데이터만 가져옴
    userdatas = db.query(Userdata.amount).filter(Userdata.transaction_type == "지출").all()    
    db.close()
    return userdatas


# 지출 or 수입의 모든 데이터를 조회하는 API
@app.get("/userdata/by-type/")
def read_userdata_by_type(transaction_type: str = Query(None)):
    db = SessionLocal()
    userdatas = db.query(Userdata).filter(Userdata.transaction_type == transaction_type).all()  # transaction_type으로 필터링
    db.close()
    return userdatas