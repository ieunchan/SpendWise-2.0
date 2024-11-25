from modules.ui_elements import display_expense_pie_chart, display_expense_line_graph, display_income_pie_chart,display_income_line_graph
from modules.api_list import GET_ANNUAL_EXPENSE_RANK, GET_ANNUAL_INCOME_RANK, GET_MONTHLY_EXPENSE_DATA,GET_MONTHLY_INCOME_DATA
from modules.utils import fetch_data
from datetime import datetime
import streamlit as st
import pandas as pd

def get_annual_data():
    type_input, year_input = st.columns(2)

    with type_input:
        transaction_type = st.selectbox("거래 유형", ["지출", "소득"], key="transaction_type_selectbox")

    with year_input:
        current_year = datetime.now().year
        year = st.selectbox("년도", list(range(current_year - 10, current_year + 1)), index=10, key="annual_select")

    if st.button("데이터 조회", key="annual_button", use_container_width=True, type='secondary'):
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
    
    total_description, description_chart  = st.columns([1,3.5])
    # 데이터가 있는지 확인하고 표시
    if annual_expense:
        total_yearly_amount = sum(item.get("total_amount", 0) for item in annual_expense)

        # 내역 별 금액 표
        with total_description:
            st.write(f"<span style='color:#C74446; font-size:24px;'> {year}년 {transaction_type}: {total_yearly_amount:,}원</span>",
                    unsafe_allow_html=True)
            # description별 지출 내역 표시
            for item in annual_expense:
                description = item.get("description")
                total_amount = item.get("total_amount")
                st.write(f"- {description}: {total_amount:,}원")

        # 내역 별 지출 파이차트
        with description_chart:
            with st.container():
                chart_data = pd.DataFrame(annual_expense)
                display_expense_pie_chart(chart_data, title="지출 차트")


        # 월별 지출 
        with st.container(border=True):
            monthly_expense_amount = fetch_data(GET_MONTHLY_EXPENSE_DATA, params=params)
            expense_line_graph_data = pd.DataFrame(monthly_expense_amount)
            display_expense_line_graph(expense_line_graph_data)

    else:
        st.write("데이터를 불러오지 못했습니다.")

# 년간 소득정보 한눈에 보기
def display_annual_income_data(params, year, transaction_type):
    try:
        annual_income_data = fetch_data(GET_ANNUAL_INCOME_RANK, params=params)

        total_income_amount, income_description_chart = st.columns([1, 2])  # 비율: 1:2
        if annual_income_data:

            total_yearly_amount = sum(item.get("total_amount", 0) for item in annual_income_data)

            with total_income_amount:
                st.write(f"<span style='color:#1E90FF; font-size:24px;'>{year}년 {transaction_type} 합계 : {total_yearly_amount:,} 원</span>",
                unsafe_allow_html=True)

                for item in annual_income_data:
                    description = item.get("description")
                    total_amount = item.get("total_amount")
                    st.write(f"- {description}: {total_amount:,}원")

            with income_description_chart:
                with st.container():
                    # 데이터프레임 열 이름을 변경
                    chart_data = pd.DataFrame(annual_income_data).rename(
                        columns={"description": "내역", "total_amount": "금액"})
                    display_income_pie_chart(chart_data, title="내역 별 차트")

            # 월별 그래프
            with st.container(border=True):
                monthly_income_data = fetch_data(GET_MONTHLY_INCOME_DATA, params=params)
                display_income_line_graph(monthly_income_data)

        else:
            st.write("데이터 로드 중 에러가 발생했습니다.")


    except ValueError as e:
        # API 요청 실패 시 에러 메시지 표시
        st.error(f"데이터 요청 실패: {e}")


