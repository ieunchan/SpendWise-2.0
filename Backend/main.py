from fastapi import FastAPI, HTTPException
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