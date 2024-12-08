from modules.api_list import GET_USERDATA_EXPENSE, GET_USERDATA_INCOME, GET_EXPENSE_RANKING, GET_EXPENSE_DETAILS, GET_INCOME_RANKING
from modules.ui_elements import display_expense_pie_chart, display_income_pie_chart
from modules.utils import fetch_data
from datetime import datetime
import streamlit as st
import time
import pandas as pd

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
    if st.button("데이터 조회", key="for monthly data", use_container_width=True, type='secondary'):
        st.session_state.monthly_data_fetched = True
        st.session_state.monthly_params = {"year": year, "month": month}
        st.session_state.monthly_show_details = False  # 상세 조회 초기화

    # 데이터 표시
    if st.session_state.monthly_data_fetched:
        params = st.session_state.monthly_params
        show_expense_amount_rank, show_income_amount = st.columns(2)
        show_expense_pie_chart, show_income_pie_chart = st.columns([1,1.3])

        with show_expense_amount_rank:
            with st.container(border=True):
                display_expense_amount_rank(params, year, month)
        with show_income_amount:
            with st.container(border=True):
                display_income_amount_rank(params, year, month)
        with show_expense_pie_chart:
            with st.container(border=True):
                display_month_expense_pie_chart(params)
        with show_income_pie_chart:
            with st.container(border=True):
                display_month_income_pie_chart(params)
        with st.container(border=True):
            display_expense_details(params)


def display_expense_amount_rank(params, year, month):
    """지출 데이터를 조회하고 결과를 Streamlit에 표시하는 함수"""
    # 지출 데이터 가져오기
    expense_data = fetch_data(GET_USERDATA_EXPENSE, params=params)
    total_expense = sum(expense['amount'] for expense in expense_data)
    st.markdown(
        f"<span style='color:#C74446; font-size:24px;'>{year}년 {month}월 지출 : {total_expense:,} 원</span>",
        unsafe_allow_html=True)
    # 지출 랭킹 데이터 가져오기
    rank_data = fetch_data(GET_EXPENSE_RANKING, params=params)

    for i, item in enumerate(rank_data, start=1):
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


def display_month_expense_pie_chart(params):
    data = pd.DataFrame(fetch_data(GET_EXPENSE_RANKING, params=params))
    display_expense_pie_chart(data, title="지출 차트")

def display_month_income_pie_chart(params):
    income_pie_data = pd.DataFrame(fetch_data(GET_INCOME_RANKING, params=params))
    display_income_pie_chart(income_pie_data, title="소득 차트")

def display_expense_details(params):
    # radio 버튼으로 항목 선택
    st.markdown("#### 자세히 볼 항목을 선택하세요")
    data = pd.DataFrame(fetch_data(GET_EXPENSE_RANKING, params=params))
    selected_category = st.selectbox(
        label="상세내역",
        options=data["description"].unique(),
        index=0  # 기본값으로 첫 번째 항목 선택
    )

    # description 추가
    detail_params = {**params, "description": selected_category}

    # Fetch 데이터
    # 시작 시간
    total_start_time = time.time()

    # 데이터 가져오기 시간 측정
    fetch_start_time = time.time()
    expense_details = fetch_data(GET_EXPENSE_DETAILS, params=detail_params)
    fetch_end_time = time.time()

    # 데이터 처리 시간 측정
    process_start_time = time.time()
    if expense_details:
        detail_dataframe = pd.DataFrame(expense_details)
        detail_dataframe['금액'] = detail_dataframe['금액'].apply(lambda x: f"{x:,}")
    process_end_time = time.time()

    # 화면 렌더링 시간 측정
    render_start_time = time.time()
    if expense_details:
        st.markdown(f"### {selected_category} 상세 내역")
        st.table(detail_dataframe)
    else:
        st.write(f"{selected_category}에 대한 상세 내역이 없습니다.")
    render_end_time = time.time()

    # 전체 종료 시간
    total_end_time = time.time()

    # 단계별 시간 출력
    fetch_time = fetch_end_time - fetch_start_time
    process_time = process_end_time - process_start_time
    render_time = render_end_time - render_start_time
    total_time = total_end_time - total_start_time

    st.markdown(f"**데이터 가져오기 시간**: {fetch_time:.2f}초")
    st.markdown(f"**데이터 처리 시간**: {process_time:.2f}초")
    st.markdown(f"**화면 렌더링 시간**: {render_time:.2f}초")
    st.markdown(f"**총 소요 시간**: {total_time:.2f}초")


