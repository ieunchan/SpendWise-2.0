from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Userdata
from app.utils import get_month_range
from sqlalchemy.sql import func, and_
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.schemas import ExpenseSummary

# 지출 관련 API들이 모여있습니다.

router = APIRouter()

# 지출 데이터 조회 API (총 금액만 반환)
@router.get("/", response_model=List[dict])
def read_user_expense_amount(
    year: int = Query(..., description="조회할 년도"),
    month: int = Query(..., description="조회할 월"),
    db: Session = Depends(get_db)
):
    try:
        start_of_month, end_of_month = get_month_range(year, month)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 연도 또는 월입니다.")
    
    expense_amount = (
        db.query(Userdata.amount)
        .filter(Userdata.transaction_type == "지출")
        .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
        .all()
    )
    expense_datas = [{"amount": amount[0]} for amount in expense_amount]
    return expense_datas


# 지출 금액의 순위 조회 API
@router.get("/ranking/", response_model=List[dict])
def expense_ranking(
    year: int = Query(..., description="조회할 연도"),
    month: int = Query(..., description="조회할 월"),
    db: Session = Depends(get_db)
):
    start_of_month, end_of_month = get_month_range(year, month)

    try:
        expense_rank = (
            db.query(Userdata.description, func.sum(Userdata.amount).label("total_amount"))
            .filter(
                Userdata.transaction_type == "지출",Userdata.date >= start_of_month, 
                Userdata.date < end_of_month
            )
            .group_by(
                Userdata.description
            )
            .order_by(
                func.sum(Userdata.amount).desc()
            )
            .all()
        )
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="지출 랭킹 데이터베이스 쿼리 중 오류가 발생했습니다.")

    if not expense_rank:
        return [{"description": "데이터 없음", "total_amount": 0}]
    
    expense_rank_data = [
        {
            "description": item[0] if len(item) > 0 else "데이터 없음",
            "total_amount": item[1] if len(item) > 1 else 0
        }
        for item in expense_rank
    ]
    return expense_rank_data


# 지출 항목별 상세 내역 조회 API
@router.get("/details/", response_model=List[dict])
def get_expense_details(
    year: int = Query(..., description="조회할 년도"),
    month: int = Query(..., description="조회할 월"),
    description: str = Query(..., description="지출 항목 이름"),
    db: Session = Depends(get_db)
):
    start_of_month, end_of_month = get_month_range(year, month)

    expense_details = (
        db.query(Userdata.description, Userdata.date, Userdata.description_detail, Userdata.amount)
        .filter(Userdata.description == description)
        .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
        .all()
    )
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


# 년간 지출 합계를 반환하는 API
@router.get("/annual", response_model=List[ExpenseSummary])
def get_annual_expense_by_description(
    year: int = Query(..., description="조회할 연도"),
    db: Session = Depends(get_db)
):
    try:
        annual_expense = (
            db.query(Userdata.description, func.sum(Userdata.amount).label("total_amount"))
            .filter(
                    Userdata.transaction_type == '지출',
                    Userdata.date >= f"{year}-01-01",
                    Userdata.date < f"{year+1}-01-01",
                )
            .group_by(Userdata.description)
            .order_by(func.sum(Userdata.amount).desc())
            .all()
        )

        if not annual_expense:
            return [{"description": "데이터 없음", "total_amount": 0}]
        
        annual_expense_data = [
            ExpenseSummary(description=item[0], total_amount=item[1])
            for item in annual_expense
        ]
        return annual_expense_data
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="연도별 데이터베이스 쿼리 중 오류가 발생했습니다.")


# # 월별 지출 API
# @router.get("/monthly", response_model=List[dict])
# def get_annual_monthly_expense_total(
#     year: int = Query(..., description="조회할 년도"),
#     db: Session = Depends(get_db)
# ):
#     try:
#         month_total = []
#         for month in range(1, 13):
#             start_of_month, end_of_month = get_month_range(year, month)
#             monthly_total = (
#                 db.query(func.sum(Userdata.amount).label('total_amount'))
#                 .filter(Userdata.transaction_type == "지출")
#                 .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
#                 .scalar()
#             )
#             if monthly_total is None:
#                 monthly_total = 0
#             month_total.append({
#                 "year": year,
#                 "month": month,
#                 "total_amount": monthly_total
#             })
#         return month_total
#     except SQLAlchemyError as e:
#         print(f"SQLAlchemy Error: {str(e)}")
#         raise HTTPException(status_code=500, detail="월별 지출 합계 계산 중 오류가 발생했습니다.")