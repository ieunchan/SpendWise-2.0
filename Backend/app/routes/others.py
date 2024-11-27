from fastapi import APIRouter, Query, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.database import get_db
from app.models import Userdata
from app.utils import get_month_range
from app.schemas import UserdataResponse, UserdataCreate

# 기타 API(총액, 모든 데이터)를 반환하는 API들이 모여있습니다.

router = APIRouter()

# 유저의 총 자산(총 소득 - 총 지출)을 반환하는 API
@router.get("/total_asset/", response_model=List[dict])
def show_total_asset(
    db: Session = Depends(get_db)
):
    try:
        total_asset = []
        total_income = (
            db.query(func.sum(Userdata.amount).label("total_income"))
            .filter(Userdata.transaction_type == "소득")
            .scalar()
        )
        if total_income is None:
            total_income = 0

        total_expense = (
            db.query(func.sum(Userdata.amount).label("total_expense"))
            .filter(Userdata.transaction_type == "지출")
            .scalar()
        )
        if total_expense is None:
            total_expense = 0

        total_asset.append({'total_asset': total_income - total_expense})
        return total_asset

    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="총 자산 합계 계산 중 오류가 발생했습니다.")


# 모든 데이터를 가져오는 API
@router.get("/all_data/", response_model=List[UserdataResponse])
def income_expense_all_data(
    year: int = Query(..., description="조회할 년도"),
    month: int = Query(..., description="조회할 월"),
    transaction_type: str = Query(..., description="거래내역"),
    db: Session = Depends(get_db)
):
    try:
        start_of_month, end_of_month = get_month_range(year, month)
        response_data = (
            db.query(Userdata)
            .filter(Userdata.transaction_type == transaction_type)
            .filter(Userdata.date >= start_of_month, Userdata.date < end_of_month)
            .order_by(Userdata.id.desc())
            .all()
        )
        return response_data

    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="데이터 조회 중 오류가 발생했습니다.")


# 데이터 삭제 API
@router.delete("/delete/")
def delete_data(
    id: int = Query(..., description="삭제할 데이터의 id"),
    db: Session = Depends(get_db)
):
    db_userdata = db.query(Userdata).filter(Userdata.id == id).first()

    if not db_userdata:
        raise HTTPException(status_code=404, detail="데이터가 존재하지 않습니다.")

    try:
        db.delete(db_userdata)
        db.commit()
        return {"message": "데이터가 성공적으로 제거되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"삭제 중 오류가 발생했습니다: {str(e)}")


# 데이터 생성 API
@router.post("/", response_model=UserdataResponse)
def create_userdata(userdata: UserdataCreate, db: Session = Depends(get_db)):
    db_userdata = Userdata(**userdata.model_dump())
    db.add(db_userdata)
    db.commit()
    db.refresh(db_userdata)
    return db_userdata


# 데이터 수정 API
@router.put("/update/", response_model=UserdataResponse)
def update_userdata(
    id: int = Query(..., description="조회할 id"),
    userdata: UserdataCreate = Body(...),  # 요청 본문으로 처리
    db: Session = Depends(get_db)
):
    db_userdata = db.query(Userdata).filter(Userdata.id == id).first()

    if not db_userdata:
        raise HTTPException(status_code=404, detail="해당 데이터가 존재하지 않습니다.")

    # 데이터 업데이트
    db_userdata.transaction_type = userdata.transaction_type
    db_userdata.description = userdata.description
    db_userdata.description_detail = userdata.description_detail
    db_userdata.amount = userdata.amount
    db_userdata.date = userdata.date

    # 변경 사항 커밋
    db.commit()
    db.refresh(db_userdata)

    return db_userdata