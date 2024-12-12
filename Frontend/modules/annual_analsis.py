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
        year = st.selectbox("년도", list(range(current_year, current_year - 10, -1)), index=0, key="annual_select")

    if st.button("데이터 조회", key="annual_button", use_container_width=True, type='primary'):

        annual_params = {"year": year} # API 요청 파라미터
        
        # 최적화 용도입니다. 이 API가 한 페이지에서 두번 호출되길래 한번 호출해서 변수에 담는 용도입니다. 이 변수에는 연간 총 지출이 담깁니다.
        annual_expense_rank_api = fetch_data(GET_ANNUAL_EXPENSE_RANK, params=annual_params)

        # 최적화 용도입니다. 연간 총 소득이 담기는 변수입니다. 변수를 할당함으로써 기존 2번 호출되던 API가 한번만 호출됩니다.
        annual_income_rank_api = fetch_data(GET_ANNUAL_INCOME_RANK, params=annual_params)

        # 화면에 지출/소득 을 나누기 위한 작업입니다. 이 부분은 총 지출/소득, 순위 등이 표시됩니다.
        annual_expense_description_data_total, annual_income_description_data_total = st.columns(2)

        # 지출/소득을 나누고, 지출/소득 파이차트를 위해 나누는 컬럼입니다.
        annual_expense_pie_chart, annual_income_pie_chart = st.columns([1,1.3])
        
        with annual_expense_description_data_total: # 지출: 총 지출, 지출 순위 컨테이너
            with st.container(border=True):
                display_annual_expense_description_total(year, annual_expense_rank_api)
        
        with annual_income_description_data_total: # 소득: 총 소득, 소득 순위 컨테이너
            with st.container(border=True):
                display_annual_income_description_total(year, annual_income_rank_api)

        with st.container(border=True):  # 연간 내역 별 지출 파이차트
            with annual_expense_pie_chart: 
                with st.container(border=True):
                    display_annual_expense_description_pie_chart(year, annual_expense_rank_api)

            with annual_income_pie_chart: # 연간 내역 별 소득 파이차트 컨테이너
                with st.container(border=True):
                    display_annual_income_description_pie_chart(year, annual_income_rank_api)

        with st.container(border=True): # 선택한 년도 월별 소득/지출 막대그래프 컨테이너
            expense_income_combined_bar_chart(annual_params)

# 연간 지출내역(description) 별 총액(식비: n원)
def display_annual_expense_description_total(year, annual_expense_rank_api):

        if annual_expense_rank_api:
            total_annual_amount= sum(item.get("total_amount",0) for item in annual_expense_rank_api)
        
            st.write(f"<span style='color:#C74446; font-size:24px;'> {year}년 지출: {total_annual_amount:,}원</span>", unsafe_allow_html=True)
                # description별 지출 내역 표시
            for item in annual_expense_rank_api:
                description = item.get("description")
                total_amount = item.get("total_amount")
                st.write(f"- {description}: {total_amount:,}원")
        else:
            st.write("데이터를 불러오지 못했습니다.")


def display_annual_income_description_total(year, annual_income_rank_api):
    

    if not annual_income_rank_api:
        st.write("데이터 로드 중 에러가 발생했습니다.")
        return
    total_yearly_amount = sum(item.get("total_amount", 0) for item in annual_income_rank_api)

    st.write(f"<span style='color:#1E90FF; font-size:24px;'>{year}년 소득 합계 : {total_yearly_amount:,} 원</span>",
    unsafe_allow_html=True)
    for item in annual_income_rank_api:
        description = item.get("description")
        total_amount = item.get("total_amount")
        st.write(f"- {description}: {total_amount:,}원")

# 연간 지출 내역(description) 별 파이차트
def display_annual_expense_description_pie_chart(year, annual_expense_rank_api):

        chart_data = pd.DataFrame(annual_expense_rank_api)
        display_expense_pie_chart(chart_data, title=f"{year}년 내역 별 지출")

# 연간 소득 내역 별 파이차트
def display_annual_income_description_pie_chart(year, annual_income_rank_api):

    chart_data = pd.DataFrame(annual_income_rank_api).rename(
    # 데이터프레임 열 이름을 변경
    columns={"description": "내역", "total_amount": "금액"})
    display_income_pie_chart(chart_data, title=f"{year}년 내역 별 소득")

# 수입, 지출 병합 막대 그래프
def expense_income_combined_bar_chart(annual_params):
        expense_income_monthly_data = fetch_data(GET_EXPENSE_INCOME_LINE_GRAPH_DATA, params=annual_params)
        expense_income_monthly_dataframe = pd.DataFrame(expense_income_monthly_data)
        display_combined_bar_chart(expense_income_monthly_dataframe)

