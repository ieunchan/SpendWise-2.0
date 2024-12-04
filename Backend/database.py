from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
import random
import os

Base = declarative_base()

class Userdata(Base):
    __tablename__ = "userdata"
    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String, index=True)   # 지출 또는 소득
    description = Column(String, index=True)        # 내역
    description_detail = Column(String, nullable=True)  # 기타 상세 내용
    amount = Column(Integer, index=True)            # 금액
    date = Column(Date, index=True)

# SQLite 데이터베이스 경로 설정
db_path = 'db.sqlite3'
db_uri = f'sqlite:///{db_path}'

# SQLite 데이터베이스 연결
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

# 데이터베이스 파일이 존재하지 않으면 스키마 생성
if not os.path.exists(db_path):
    Base.metadata.create_all(engine)
    print("데이터베이스 스키마를 생성했습니다.")
else:
    print("기존 데이터베이스에 연결했습니다.")

# 가능한 값의 리스트
transaction_types = ['지출', '소득']

# 지출의 경우
expenditure_descriptions = ['식비', '교통비', '쇼핑', '기타', '송금']
expenditure_description_details = ['점심 식사', '저녁 식사', '지하철 요금', '버스 요금', '옷 구매', '책 구매', '온라인 쇼핑', '친구에게 송금', '기타 지출']

# 소득의 경우
income_descriptions = ['월급 입금', '보너스 입금', '이자 수익', '투자 수익 입금', '기타 소득 입금']

# 최근 3년치 데이터 생성
start_date = date.today() - timedelta(days=3*365)
end_date = date.today()

date_range = (end_date - start_date).days

entries = []
for _ in range(1000):  # 필요한 경우 엔트리 수를 조절하세요
    entry_date = start_date + timedelta(days=random.randint(0, date_range))
    transaction_type = random.choice(transaction_types)
    
    if transaction_type == '지출':
        description = random.choice(expenditure_descriptions)
        description_detail = random.choice(expenditure_description_details)
    else:  # transaction_type == '소득'
        description = random.choice(income_descriptions)
        description_detail = None
    
    amount = random.randint(100, 100000) * 10  # 1,000원에서 1,000,000원 사이의 10의 배수 금액
    
    userdata = Userdata(
        transaction_type=transaction_type,
        description=description,
        description_detail=description_detail,
        amount=amount,
        date=entry_date
    )
    entries.append(userdata)

# 엔트리를 세션에 추가하고 커밋
session.add_all(entries)
session.commit()

print("데이터베이스에 새로운 데이터가 추가되었습니다.")