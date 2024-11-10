from modules.api_list import GET_USERDATA_EXPENSE, GET_USERDATA_INCOME, GET_EXPENSE_RANKING, GET_EXPENSE_DETAILS, GET_INCOME_RANKING
from modules.ui_elements import display_pie_chart
from modules.utils import fetch_data
from datetime import datetime
import streamlit as st
import pandas as pd

def data_analysis_page():
    """데이터 분석 페이지를 표시하는 함수"""
    # 날짜 및 데이터 종류 선택
    type_input, year_input, month_input = st.columns(3)

    with type_input:
        transaction_type = st.selectbox("조회할 데이터", ["지출", "수입"])

    with year_input:
        current_year = datetime.now().year
        year = st.selectbox("년도", list(range(current_year - 10, current_year + 1)), index=10)

    with month_input:
        current_month = datetime.now().month
        month = st.selectbox("월", list(range(1, 13)), index=current_month - 1)

    # 데이터 조회 버튼 클릭 여부를 session_state에 저장
    if "data_fetched" not in st.session_state:
        st.session_state.data_fetched = False

    # 데이터 조회 버튼을 눌렀을 때 data_fetched 상태를 True로 설정
    if st.button("데이터 조회"):
        st.session_state.data_fetched = True
        st.session_state.params = {"year": year, "month": month}
        st.session_state.transaction_type = transaction_type
        st.session_state.show_details = False  # 상세 조회 초기화

    # data_fetched가 True인 경우에만 데이터를 표시
    if st.session_state.data_fetched:
        params = st.session_state.params
        transaction_type = st.session_state.transaction_type

        if transaction_type == "지출":
            display_expense_data(params, year, month)
        elif transaction_type == "수입":
            display_income_data(params, year, month)


def display_expense_data(params, year, month):
    """지출 데이터를 조회하고 결과를 Streamlit에 표시하는 함수"""
    try:
        # 지출 데이터 가져오기
        expense_data = fetch_data(GET_USERDATA_EXPENSE, params=params)
        total_expense = sum(expense['amount'] for expense in expense_data)
        st.markdown(
            f"<span style='color:#C74446; font-size:24px;'>{year}년 {month}월 지출 : {total_expense:,} 원</span>",
            unsafe_allow_html=True)

        # 지출 랭킹 데이터 가져오기
        rank_data = fetch_data(GET_EXPENSE_RANKING, params=params)
        st.markdown(f"### {year}년 {month}월 지출 내역 순위")
        for i, item in enumerate(rank_data, start=1):
            st.write(f"{i}. {item['description']}: {item['total_amount']:,} 원")

        # 원형 그래프 생성 및 표시
        data = pd.DataFrame(rank_data)
        display_pie_chart(data, title="그래프로 보기")
        
        # radio 버튼으로 항목 선택
        st.markdown("#### 자세히 볼 항목을 선택하세요")
        selected_category = st.radio(
            label="",
            options=data["description"].unique(),
            index=0  # 기본값으로 첫 번째 항목을 선택
        )

        # 상세 내역 조회 버튼 클릭 시 show_details를 True로 설정
        if st.button("상세 내역 조회"):
            st.session_state.show_details = True
            st.session_state.selected_category = selected_category

        # show_details가 True일 때만 상세 내역을 표시
        if st.session_state.get("show_details", False):
            display_expense_details(st.session_state.selected_category, params)

    except ValueError as e:
        st.error(e)


def display_income_data(params, year, month):
    """수입 데이터를 조회하고 결과를 Streamlit에 표시하는 함수"""
    try:
        # 수입 데이터 가져오기
        income_data = fetch_data(GET_USERDATA_INCOME, params=params)
        total_income = sum(income['amount'] for income in income_data)
        st.markdown(
            f"<span style='color:#1E90FF; font-size:24px;'>{year}년 {month}월 수입 : {total_income:,} 원</span>",
            unsafe_allow_html=True)
        
        # 수입 랭킹 데이터 가져오기
        income_rank_data = fetch_data(GET_INCOME_RANKING, params=params)
        st.markdown(f"### {year}년 {month}월 수입 순위")
        for i, item in enumerate(income_rank_data, start=1):
            st.markdown(f"##### • {item['날짜']} [{item['내역']}]:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{item['금액']:,}원") # &nbsp;은 마크다운 문법에서 공백입니다.

    except ValueError as e:
        st.error(e)

def display_expense_details(selected_category, params):
    """선택된 항목에 대한 상세 내역을 표시하는 함수"""
    detail_params = {**params, "description": selected_category} # **params는 기존 params({year: year}, {month: month}에 description을 추가함)
    expense_details = fetch_data(GET_EXPENSE_DETAILS, params=detail_params)

    if expense_details:
        detail_dataframe = pd.DataFrame(expense_details)
        detail_dataframe['금액'] = detail_dataframe['금액'].apply(lambda x: f"{x:,}") # 상세보기 '금액' 부분에 세자리마다 콤마(,) 추가
        st.markdown(f"### {selected_category} 상세 내역")
        st.table(detail_dataframe)
    else:
        st.write(f"{selected_category}에 대한 상세 내역이 없습니다.")