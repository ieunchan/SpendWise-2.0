import streamlit as st
from modules.api_list import GET_TOTAL_ASSETS, GET_ANNUAL_EXPENSE_RANK
from modules.utils import fetch_data
from datetime import datetime

def total_asset_expend_income(key):
    # 데이터를 fetch_data를 통해 가져옴
    total_assets = fetch_data(GET_TOTAL_ASSETS)
    # 반환값 예시: [{"총 자산": total_assets, "총 소득": total_income, "총 지출": total_expend}]
    
    # 리스트 형태와 해당 key가 있는지 확인
    if total_assets and isinstance(total_assets, list) and key in total_assets[0]:
        # 첫 번째 항목에서 key 값에 해당하는 항목 가져오기
        total_data = total_assets[0].get(key)
        st.write(f"### {key}: {total_data:,}")  # 세 자리마다 콤마 추가
    else:
        st.write(f"{key} 데이터를 불러오지 못했습니다.")
    # total_asset_expend_income("총 자산")
    # total_asset_expend_income("총 소득")
    # total_asset_expend_income("총 지출")

def get_annual_data():
    type_input, year_input = st.columns(2)

    with type_input:
        transaction_type = st.radio("거래 유형", ["소득", "지출"], key="transaction_type_radio")

    with year_input:
        current_year = datetime.now().year
        year = st.selectbox("년도", list(range(current_year - 10, current_year + 1)), index=10, key="annual_select")

    if st.button("데이터 조회", key="annual_button"):
        # API 요청 파라미터 설정
        params = {"year": year, "transaction_type": transaction_type}
        
        # 데이터 가져오기
        annual_expense = fetch_data(GET_ANNUAL_EXPENSE_RANK, params=params)
        
        # 데이터가 있는지 확인하고 표시
        if annual_expense:
            st.write(f"### {year}년 {transaction_type} 합계")
            
            # 전체 연도의 description별 합계 표시
            total_yearly_amount = sum(item.get("total_amount", 0) for item in annual_expense)
            st.write(f"#### 총 {transaction_type} 합계: {total_yearly_amount:,}원")
            
            # description별 지출 내역 표시
            for item in annual_expense:
                description = item.get("description")
                total_amount = item.get("total_amount")
                st.write(f"- {description}: {total_amount:,}원")
        else:
            st.write("데이터를 불러오지 못했습니다.")
