import streamlit as st
import requests
from decouple import AutoConfig

config = AutoConfig()
GET_USERDATA_ALL = config("GET_USERDATA_ALL")
GET_USERDATA_EXPENSE = config("GET_USERDATA_EXPENSE")
GET_USERDATA_INCOME = config("GET_USERDATA_INCOME")

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
        response = requests.get(GET_USERDATA_EXPENSE)
        if response.status_code == 200:
            data = response.json()
            total_expense = sum(expense['amount'] for expense in data)
            st.markdown(f"### 이번달 지출 : {total_expense:,} 원")
        else:
            st.error(f"오류 발생: 상태 코드 {response.status_code}")

    elif transaction_type == "수입":
        response = requests.get(GET_USERDATA_INCOME)
        if response.status_code == 200:
            data = response.json()
            total_income = sum(income['amount'] for income in data)
            st.markdown(f"### 이번달 수입: {total_income:,} 원")
        else:
            st.error(f"오류 발생: 상태 코드 {response.status_code}")