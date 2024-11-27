from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

# 데이터베이스 테이블과 연결되는 SQLAlchemy ORM 모델을 설정합니다.

Base = declarative_base()

class Userdata(Base):
    __tablename__ = "userdata"
    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String, index=True)   # 지출 또는 소득
    description = Column(String, index=True)        # 내역
    description_detail = Column(String, nullable=True)  # 기타 상세 내용
    amount = Column(Integer, index=True)            # 금액
    date = Column(Date, index=True)