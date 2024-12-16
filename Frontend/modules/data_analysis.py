from modules.api_list import GET_USERDATA_EXPENSE, GET_USERDATA_INCOME, GET_EXPENSE_RANKING, GET_EXPENSE_DETAILS, GET_INCOME_RANKING
from modules.ui_elements import display_expense_pie_chart, display_income_pie_chart
from modules.utils import fetch_data
from datetime import datetime
import streamlit as st
import pandas as pd
import time  # 시간 측정을 위해 추가

def data_analysis_page():
    """데이터 분석 페이지를 표시하는 함수"""
    # session_state 초기화
    if "monthly_data_fetched" not in st.session_state:
        st.session_state.monthly_data_fetched = False
    if "monthly_show_details" not in st.session_state:
        st.session_state.monthly_show_details = False
    if "monthly_params" not in st.session_state:
        st.session_state.monthly_params = {}
    if "monthly_selected_category" not in st.session_state:
        st.session_state.monthly_selected_category = None

    # 날짜 및 데이터 종류 선택
    year_input, month_input = st.columns(2)

    with year_input:
        current_year = datetime.now().year
        year = st.selectbox(f"년도", list(range(current_year, current_year - 10, -1)), index=0)

    with month_input:
        current_month = datetime.now().month
        month = st.selectbox("월", list(range(12,0, -1)), index= 12-current_month)

    # 데이터 조회 버튼
    if st.button("데이터 조회", key="for monthly data", use_container_width=True, type='primary'):
        st.session_state.monthly_data_fetched = True
        st.session_state.monthly_params = {"year": year, "month": month}
        st.session_state.monthly_show_details = True  # 상세 조회 초기화



    # 데이터 표시
    if st.session_state.monthly_data_fetched:

        params = st.session_state.monthly_params

        # 월간 지출 랭킹을 담는 API. API 호출을 최소화 하기 위해 변수에 담는다.
        expense_ranking_api = fetch_data(GET_EXPENSE_RANKING, params=params)

        show_expense_amount_rank, show_income_amount = st.columns(2)

        show_expense_pie_chart, show_income_pie_chart = st.columns([1,1.3])

        with show_expense_amount_rank:
            with st.container(border=True):
                display_expense_amount_rank(params, year, month, expense_ranking_api)
        with show_income_amount:
            with st.container(border=True):
                display_income_amount_rank(params, year, month)
        with show_expense_pie_chart:
            with st.container(border=True):
                display_month_expense_pie_chart(expense_ranking_api)
        with show_income_pie_chart:
            with st.container(border=True):
                display_month_income_pie_chart(params)
        with st.container(border=True):
            display_expense_details(params, expense_ranking_api)


def display_expense_amount_rank(params, year, month, expense_ranking_api):
    """지출 데이터를 조회하고 결과를 Streamlit에 표시하는 함수"""
    # 지출 데이터 가져오기
    expense_data = fetch_data(GET_USERDATA_EXPENSE, params=params)
    total_expense = sum(expense['amount'] for expense in expense_data)
    st.markdown(
        f"<span style='color:#C74446; font-size:24px;'>{year}년 {month}월 지출 : {total_expense:,} 원</span>",
        unsafe_allow_html=True)
    # 지출 랭킹 데이터 가져오기

    for i, item in enumerate(expense_ranking_api, start=1):
        st.markdown(f"#### {i}. {item['description']}: {item['total_amount']:,} 원")

def display_income_amount_rank(params, year, month):
    """소득 데이터를 조회하고 결과를 Streamlit에 표시하는 함수"""
    # 소득 데이터 가져오기
    income_data = fetch_data(GET_USERDATA_INCOME, params=params)
    total_income = income_data.get("total_amount", 0)  # "total_amount"가 없으면 0 반환

    st.markdown(
        f"<span style='color:#1E90FF; font-size:24px;'>{year}년 {month}월 소득 : {total_income:,} 원</span>",
        unsafe_allow_html=True
    )

    # 소득 랭킹 데이터 가져오기
    income_rank_data = fetch_data(GET_INCOME_RANKING, params=params)
    for item in income_rank_data:
        st.markdown(f"##### • {item['날짜']} [{item['내역']}]: {item['금액']:,}원")


def display_month_expense_pie_chart(expense_ranking_api):

    month_expense_pie_data = pd.DataFrame(expense_ranking_api)
    display_expense_pie_chart(month_expense_pie_data, title="지출 차트")

def display_month_income_pie_chart(params):
    income_pie_data = pd.DataFrame(fetch_data(GET_INCOME_RANKING, params=params))
    display_income_pie_chart(income_pie_data, title="소득 차트")

def display_expense_details(params, expense_ranking_api):
    # radio 버튼으로 항목 선택
    st.markdown("#### 자세히 볼 항목을 선택하세요")
    data = pd.DataFrame(expense_ranking_api)
    selected_category = st.radio(
        label="상세내역",
        options=data["description"].unique(),
        index=0,  # 기본값으로 첫 번째 항목 선택
        horizontal=True
    )

    # description 추가
    detail_params = {**params, "description": selected_category}

    expense_details = fetch_data(GET_EXPENSE_DETAILS, params=detail_params)


    if expense_details:
        detail_dataframe = pd.DataFrame(expense_details)
        detail_dataframe['금액'] = detail_dataframe['금액'].apply(lambda x: f"{x:,}")
    if expense_details:
        st.markdown(f"### {selected_category} 상세 내역")
        st.table(detail_dataframe)
    else:
        st.write(f"{selected_category}에 대한 상세 내역이 없습니다.")