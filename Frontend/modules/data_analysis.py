import streamlit as st
import requests
from decouple import AutoConfig

config = AutoConfig()
GET_USERDATA_ALL = config("GET_USERDATA_ALL")
GET_USERDATA_EXPENSE = config("GET_USERDATA_EXPENSE")
GET_USERDATA_INCOME = config("GET_USERDATA_INCOME")
GET_EXPENSE_RANKING = config("GET_EXPENSE_RANKING")

def data_analysis_page():
    transaction_type = st.selectbox("조회할 데이터", ["지출/수입 선택", "지출", "수입"])

    if transaction_type == "지출/수입 선택":
        response = requests.get(GET_USERDATA_ALL)
        if response.status_code == 200:
            data = response.json()
            st.write(data)
        else:
            st.error("데이터를 가져오지 못했습니다.")

    elif transaction_type == "지출":
        # 1. 지출 데이터 요청 및 처리
        expense_response = requests.get(GET_USERDATA_EXPENSE)
        if expense_response.status_code == 200:
            try:
                expense_data = expense_response.json()
                # 모든 지출의 합계를 계산하고 포맷하여 출력
                total_expense = sum(expense['amount'] for expense in expense_data)
                st.markdown(f"### 이번달 지출 : {total_expense:,} 원")
            except Exception as e:
                st.error(f"지출 데이터 처리 중 오류 발생: {e}")
        else:
            st.error(f"지출 데이터 요청 오류: 상태 코드 {expense_response.status_code}")
    
        # 2. 지출 랭킹 데이터 요청 및 처리
        rank_response = requests.get(GET_EXPENSE_RANKING)
        if rank_response.status_code == 200:
            try:
                rank_data = rank_response.json()
                sorted_rank_data = sorted(rank_data, key=lambda x: x['total_amount'],reverse=True)
                st.markdown("### 지출 내역별 랭킹")
                for i, item in enumerate(sorted_rank_data, start=1):
                    st.write(f"{i}. {item['description']}: {item['total_amount']:,} 원")
            except Exception as e:
                st.error(f"랭킹 데이터 처리 중 오류 발생: {e}")
        else:
            st.error(f"랭킹 데이터 요청 오류: 상태 코드 {rank_response.status_code}")


    elif transaction_type == "수입":
        response = requests.get(GET_USERDATA_INCOME)
        if response.status_code == 200:
            data = response.json()
            total_income = sum(income['amount'] for income in data)
            st.markdown(f"### 이번달 수입: {total_income:,} 원")
        else:
            st.error(f"오류 발생: 상태 코드 {response.status_code}")