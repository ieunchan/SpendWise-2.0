from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Userdata
from app.utils import get_month_range
from sqlalchemy.sql import func, and_
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.schemas import ExpenseSummary

# 소득 관련 API들이 모여있습니다.

router = APIRouter()

# 소득 데이터 조회 API (총 금액만 반환)
@router.get("/", response_model=List[dict])
def read_user_income_amount(
    year: int = Query(..., description="조회할 년도"),
    month: int = Query(..., description="조회할 월"),
    db: Session = Depends(get_db)
):
    try:
        start_of_month, end_of_month = get_month_range(year, month)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 연도 또는 월입니다.")

    income_amount = (
        db.query(Userdata.amount)
        .filter(Userdata.transaction_type == "소득")
        .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
        .all()
    )

    income_datas = [{"amount": amount[0]} for amount in income_amount]
    return income_datas


# 선택한 년도, 월의 순위 데이터를 반환하는 API
@router.get("/ranking/", response_model=List[dict])
def income_ranking(
    year: int = Query(..., description="조회할 년도"),
    month: int = Query(..., description="조회할 월"),
    db: Session = Depends(get_db)
):
    start_of_month, end_of_month = get_month_range(year, month)

    try:
        income_rank = (
            db.query(Userdata)
            .filter(Userdata.transaction_type == "소득")
            .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
            .order_by(Userdata.date.desc())
            .all()
        )
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="소득 랭킹 데이터베이스 쿼리 중 오류가 발생했습니다.")

    if not income_rank:
        return [{"날짜": "데이터 없음", "내역": "내역 없음", "금액": 0}]

    income_rank_data = [
        {
            "날짜": income.date.strftime("%Y-%m-%d"),
            "내역": income.description,
            "금액": income.amount
        }
        for income in income_rank
    ]
    return income_rank_data


# 년간 소득 합계를 반환하는 API
@router.get("/annual", response_model=List[ExpenseSummary])
def get_annual_income(
    year: int = Query(..., description="조회할 년도"),
    transaction_type: str = Query(..., description="년도 별 소득"),
    db: Session = Depends(get_db)
):
    try:
        annual_income = (
            db.query(Userdata.description, func.sum(Userdata.amount).label("total_amount"))
            .filter(
                and_(
                    Userdata.transaction_type == transaction_type,
                    func.extract('year', Userdata.date) == year
                )
            )
            .group_by(Userdata.description)
            .order_by(func.sum(Userdata.amount).desc())
            .all()
        )

        if not annual_income:
            return [{"description": "데이터 없음", "total_amount": 0}]

        annual_income_data = [
            ExpenseSummary(description=item[0], total_amount=item[1])
            for item in annual_income
        ]
        return annual_income_data
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="연도별 데이터베이스 쿼리 중 오류가 발생했습니다.")


# 월별 소득 API
@router.get("/monthly", response_model=List[dict])
def get_annual_monthly_income_total(
    year: int = Query(..., description="조회할 년도"),
    db: Session = Depends(get_db)
):
    try:
        month_total = []
        for month in range(1, 13):
            start_of_month, end_of_month = get_month_range(year, month)
            monthly_total = (
                db.query(func.sum(Userdata.amount).label("total_amount"))
                .filter(Userdata.transaction_type == "소득")
                .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
                .scalar()
            )
            if monthly_total is None:
                monthly_total = 0

            month_total.append({
                "year": year,
                "month": month,
                "total_amount": monthly_total
            })
        return month_total
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="월별 소득 합계 계산 중 오류가 발생했습니다.")