from modules.api_list import GET_TOTAL_ASSETS, GET_ANNUAL_EXPENSE_RANK, GET_ANNUAL_INCOME_RANK, GET_MONTHLY_EXPENSE_DATA
from modules.utils import fetch_data
from datetime import datetime
from modules.ui_elements import display_expense_pie_chart, display_expense_line_graph
import pandas as pd
import streamlit as st

def get_annual_data():
    type_input, year_input = st.columns(2)

    with type_input:
        transaction_type = st.radio("거래 유형", ["지출", "소득"], key="transaction_type_radio")

    with year_input:
        current_year = datetime.now().year
        year = st.selectbox("년도", list(range(current_year - 10, current_year + 1)), index=10, key="annual_select")

    if st.button("데이터 조회", key="annual_button"):
        # API 요청 파라미터 설정
        params = {"year": year, "transaction_type": transaction_type}
        year = year
        transaction_type = transaction_type

        if transaction_type == "지출":
            display_annual_expense_data(params, year, transaction_type)
        elif transaction_type == "소득":
            display_annual_income_data(params, year, transaction_type)

# 년간 지출정보 한눈에 보기
def display_annual_expense_data(params, year, transaction_type):
    # 데이터 가져오기
    annual_expense = fetch_data(GET_ANNUAL_EXPENSE_RANK, params=params)
    
    total_description, description_chart  = st.columns(2)
    # 데이터가 있는지 확인하고 표시
    if annual_expense:
        total_yearly_amount = sum(item.get("total_amount", 0) for item in annual_expense)

        # 내역 별 금액 표
        with total_description:
            st.write(f"<span style='color:#C74446; font-size:24px;'> {year}년 {transaction_type} 합계: {total_yearly_amount:,}원</span>",
                    unsafe_allow_html=True)
            # description별 지출 내역 표시
            for item in annual_expense:
                description = item.get("description")
                total_amount = item.get("total_amount")
                st.write(f"- {description}: {total_amount:,}원")

        # 내역 별 지출 파이차트
        with description_chart:
            chart_data = pd.DataFrame(annual_expense)
            display_expense_pie_chart(chart_data, title="지출 차트")


        # 월별 지출 
        monthly_expense_amount = fetch_data(GET_MONTHLY_EXPENSE_DATA, params=params)
        expense_line_graph_data = pd.DataFrame(monthly_expense_amount)
        display_expense_line_graph(expense_line_graph_data)

    else:
        st.write("데이터를 불러오지 못했습니다.")

# 년간 소득정보 한눈에 보기
def display_annual_income_data(params, year, transaction_type):
    try:
        annual_income_data = fetch_data(GET_ANNUAL_INCOME_RANK, params=params)

        if annual_income_data:
            st.write(f"### {year}년 {transaction_type} 합계")
            
            for amount in annual_income_data:
                year = amount.get("year")
                total_amount = amount.get("total_amount")[0] # 리스트 형태에서 3자리 마다 소수점을 붙히기 어려워서 리스트의 0번 값을 빼와서 숫자로 바꿈
                st.markdown(f"### {total_amount:,} 원")
        
        else:
            st.write("데이터 로드 중 에러가 발생했습니다.")


    except ValueError as e:
        # API 요청 실패 시 에러 메시지 표시
        st.error(f"데이터 요청 실패: {e}")


