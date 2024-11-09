import streamlit as st
import requests
from decouple import AutoConfig
from datetime import datetime

config = AutoConfig()
GET_USERDATA_EXPENSE = config("GET_USERDATA_EXPENSE")
GET_USERDATA_INCOME = config("GET_USERDATA_INCOME")
GET_EXPENSE_RANKING = config("GET_EXPENSE_RANKING")

def data_analysis_page():
    type_input, year_input, month_input = st.columns(3)

    with type_input:
        transaction_type = st.selectbox("조회할 데이터", ["지출", "수입"])

    with year_input:
        current_year = datetime.now().year
        year = st.selectbox("년", list(range(current_year - 10, current_year + 1)), index=10)

    with month_input:
        current_month = datetime.now().month
        month = st.selectbox("월", list(range(1, 13)), index=current_month - 1)

    # 데이터 조회 요청 버튼
    if st.button("데이터 조회"):
        # 선택한 연도와 월을 쿼리 파라미터로 설정
        params = {"year": year, "month": month}

        if transaction_type == "지출":
            # 지출 데이터 요청 및 처리
            expense_response = requests.get(GET_USERDATA_EXPENSE, params=params)
            if expense_response.status_code == 200:
                try:
                    expense_data = expense_response.json()
                    total_expense = sum(expense['amount'] for expense in expense_data)
                    st.markdown(f"### {year}년 {month}월 지출 : {total_expense:,} 원")
                except Exception as e:
                    st.error(f"지출 데이터 처리 중 오류 발생: {e}")
            else:
                st.error(f"지출 데이터 요청 오류: 상태 코드 {expense_response.status_code}")

            # 지출 랭킹 데이터 요청 및 처리
            rank_response = requests.get(GET_EXPENSE_RANKING, params=params)
            if rank_response.status_code == 200:
                try:
                    rank_data = rank_response.json()
                    st.markdown(f"### {year}년 {month}월 지출 내역별 랭킹")
                    for i, item in enumerate(rank_data, start=1):
                        st.write(f"{i}. {item['description']}: {item['total_amount']:,} 원")
                except Exception as e:
                    st.error(f"랭킹 데이터 처리 중 오류 발생: {e}")
            else:
                st.error(f"랭킹 데이터 요청 오류: 상태 코드 {rank_response.status_code}")

        elif transaction_type == "수입":
            # 수입 데이터 요청 및 처리
            income_response = requests.get(GET_USERDATA_INCOME, params=params)
            if income_response.status_code == 200:
                try:
                    income_data = income_response.json()
                    total_income = sum(income['amount'] for income in income_data)
                    st.markdown(f"### {year}년 {month}월 수입: {total_income:,} 원")
                except Exception as e:
                    st.error(f"수입 데이터 처리 중 오류 발생: {e}")
            else:
                st.error(f"수입 데이터 요청 오류: 상태 코드 {income_response.status_code}")