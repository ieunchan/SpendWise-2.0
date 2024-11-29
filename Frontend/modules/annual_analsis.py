from modules.ui_elements import display_expense_pie_chart, display_income_pie_chart, display_combined_bar_chart
from modules.api_list import GET_ANNUAL_EXPENSE_RANK, GET_ANNUAL_INCOME_RANK, GET_EXPENSE_INCOME_LINE_GRAPH_DATA
from modules.utils import fetch_data
from datetime import datetime
import streamlit as st
import pandas as pd

def get_annual_data():
    year_input = st.columns(1)[0]

    with year_input:
        current_year = datetime.now().year
        year = st.selectbox("년도", list(range(current_year - 10, current_year + 1)), index=10, key="annual_select")

    if st.button("데이터 조회", key="annual_button", use_container_width=True, type='secondary'):
        annual_params = {"year": year} # API 요청 파라미터

        annual_expense_description_data_total, annual_income_description_data_total = st.columns(2)
        annual_expense_pie_chart, annual_income_pie_chart = st.columns(2)
        
        with annual_expense_description_data_total: # 연간 지출내역 별 지출 순위 
            with st.container(border=True):
                display_annual_expense_description_total(annual_params, year)
        
        with annual_income_description_data_total:
            with st.container(border=True):
                display_annual_income_description_total(annual_params,year)

        with st.container(border=True):
            with annual_expense_pie_chart: # 연간 내역 별 지출 파이차트
                with st.container(border=True):
                    display_annual_expense_description_pie_chart(annual_params,year)

            with annual_income_pie_chart: # 연간 내역 별 소득 파이차트
                with st.container(border=True):
                    display_annual_income_description_pie_chart(annual_params, year)

        with st.container(border=True): # 선택한 년도 월별 소득/지출 막대그래프
            expense_income_combined_bar_chart(annual_params)

# 연간 지출내역(description) 별 총액(식비: n원)
def display_annual_expense_description_total(annual_params, year):
        annual_expense_description_total = fetch_data(GET_ANNUAL_EXPENSE_RANK, params=annual_params)

        if annual_expense_description_total:
            total_annual_amount= sum(item.get("total_amount",0) for item in annual_expense_description_total)
        
            st.write(f"<span style='color:#C74446; font-size:24px;'> {year}년 지출: {total_annual_amount:,}원</span>", unsafe_allow_html=True)
                # description별 지출 내역 표시
            for item in annual_expense_description_total:
                description = item.get("description")
                total_amount = item.get("total_amount")
                st.write(f"- {description}: {total_amount:,}원")
        else:
            st.write("데이터를 불러오지 못했습니다.")


def display_annual_income_description_total(annual_params, year):
    annual_income_data = fetch_data(GET_ANNUAL_INCOME_RANK, params=annual_params)
    if annual_income_data:
        total_yearly_amount = sum(item.get("total_amount", 0) for item in annual_income_data)
        st.write(f"<span style='color:#1E90FF; font-size:24px;'>{year}년 소득 합계 : {total_yearly_amount:,} 원</span>",
        unsafe_allow_html=True)
        for item in annual_income_data:
            description = item.get("description")
            total_amount = item.get("total_amount")
            st.write(f"- {description}: {total_amount:,}원")
    else:
        st.write("데이터 로드 중 에러가 발생했습니다.")

# 연간 지출 내역(description) 별 파이차트
def display_annual_expense_description_pie_chart(annual_params,year):
        annual_expense_description_pie_chart = fetch_data(GET_ANNUAL_EXPENSE_RANK, params=annual_params)
        chart_data = pd.DataFrame(annual_expense_description_pie_chart)
        display_expense_pie_chart(chart_data, title=f"{year}년 내역 별 지출")

# 연간 소득 내역 별 파이차트
def display_annual_income_description_pie_chart(annual_params,year):
    annual_income_description_pie_chart = fetch_data(GET_ANNUAL_INCOME_RANK, params=annual_params)
    chart_data = pd.DataFrame(annual_income_description_pie_chart).rename(
    # 데이터프레임 열 이름을 변경
    columns={"description": "내역", "total_amount": "금액"})
    display_income_pie_chart(chart_data, title=f"{year}년 내역 별 소득")

# 수입, 지출 병합 막대 그래프
def expense_income_combined_bar_chart(annual_params):
        expense_income_monthly_data = fetch_data(GET_EXPENSE_INCOME_LINE_GRAPH_DATA, params=annual_params)
        expense_income_monthly_dataframe = pd.DataFrame(expense_income_monthly_data)
        display_combined_bar_chart(expense_income_monthly_dataframe)

