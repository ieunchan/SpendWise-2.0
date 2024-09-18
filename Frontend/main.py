import streamlit as st
import requests
from datetime import date
from decouple import AutoConfig

config = AutoConfig()

# FastAPI 백엔드 URL
BACKEND_URL = config("BACKEND_URL")

st.title("지출 관리 시스템")

# 사용자 입력을 위한 Form
with st.form(key="expense_form"):
    transaction_type = st.selectbox("거래 유형", ["지출", "수입"])
    description = st.text_input("내역")
    amount = st.number_input("금액", min_value=0)
    date_input = st.date_input("날짜", value=date.today())
    
    # 제출 버튼
    submit_button = st.form_submit_button(label="제출")

# 폼 제출 시 처리 로직
if submit_button:
    # 백엔드로 전송할 데이터 준비
    userdata = {
        "transaction_type": transaction_type,
        "description": description,
        "amount": amount,
        "date": str(date_input)
    }

    # FastAPI 백엔드로 POST 요청 보내기
    response = requests.post(BACKEND_URL, json=userdata)

    # 요청 결과 출력
    if response.status_code == 200:
        st.success("데이터가 성공적으로 저장되었습니다.")
        st.json(response.json())  # 저장된 데이터 출력
    else:
        st.error(f"오류 발생: {response.status_code}")
        st.write(response.text)