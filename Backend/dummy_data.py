from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date, timedelta
from decouple import AutoConfig
import random

Base = declarative_base()

class Userdata(Base):
    __tablename__ = "userdata"
    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String, index=True)
    description = Column(String, index=True)
    description_detail = Column(String, nullable=True)
    amount = Column(Integer, index=True)
    date = Column(Date, index=True)

# .env 파일에서 환경 변수 로드
config = AutoConfig()

DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME")

db_uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"Database URI: {db_uri}")

# PostgreSQL 연결
try:
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    # 테이블 생성
    Base.metadata.create_all(engine)
    print("테이블 생성 완료")

    # 랜덤 데이터 생성 및 삽입
    transaction_types = ['지출', '소득']
    expenditure_descriptions = ['식비', '교통비', '쇼핑', '기타', '송금']
    expenditure_description_details = ['점심 식사', '저녁 식사', '지하철 요금', '버스 요금', '옷 구매', '책 구매', '온라인 쇼핑', '친구에게 송금', '기타 지출']
    income_descriptions = ['월급 입금', '보너스 입금', '이자 수익', '투자 수익 입금', '기타 소득 입금']

    start_date = date.today() - timedelta(days=3*365)
    end_date = date.today()
    date_range = (end_date - start_date).days

    entries = []
    for _ in range(1000):
        entry_date = start_date + timedelta(days=random.randint(0, date_range))
        transaction_type = random.choice(transaction_types)

        if transaction_type == '지출':
            description = random.choice(expenditure_descriptions)
            description_detail = random.choice(expenditure_description_details)
        else:
            description = random.choice(income_descriptions)
            description_detail = None

        amount = random.randint(100, 100000) * 10

        userdata = Userdata(
            transaction_type=transaction_type,
            description=description,
            description_detail=description_detail,
            amount=amount,
            date=entry_date
        )
        entries.append(userdata)

    session.add_all(entries)
    session.commit()
    print("데이터 삽입 완료")
except Exception as e:
    print(f"오류 발생: {e}")
finally:
    session.close()