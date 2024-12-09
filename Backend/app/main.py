from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from app.routes import expense, income, others

# FastAPI 인스턴스 생성
app = FastAPI()

# CORS 설정
origins = [
    "https://spendwise.streamlit.app",  # Streamlit 배포 URL
    "https://d792-124-60-151-80.ngrok-free.app",  # Ngrok URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 출처
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용 (GET, POST 등)
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# 응답 시간 측정 미들웨어
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()  # 요청 시작 시간
    response = await call_next(request)  # 요청 처리
    end_time = time.perf_counter()  # 요청 완료 시간
    process_time = end_time - start_time  # 처리 시간 계산
    response.headers["X-Process-Time"] = f"{process_time:.4f}"  # 응답 헤더에 처리 시간 추가
    return response

# 라우터 등록
app.include_router(expense.router, prefix="/userdata/expense", tags=["Expense"])
app.include_router(income.router, prefix="/userdata/income", tags=["Income"])
app.include_router(others.router, prefix="/userdata", tags=["Others"])