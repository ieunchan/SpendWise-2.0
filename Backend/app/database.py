from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from decouple import AutoConfig

# 데이터베이스 연결 및 ORM을 설정하는 파일입니다.

config = AutoConfig()
# DATABASE_URL = config("DATABASE_URL")


# 환경 변수 가져오기
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 세션 의존성 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 테이블 생성
Base.metadata.create_all(bind=engine)