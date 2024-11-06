import streamlit as st
import requests
from datetime import date
from decouple import AutoConfig

config = AutoConfig()

# FastAPI 백엔드 URL
DATA_CREATE = config("DATA_CREATE") # 데이터 입력 api
GET_USERDATA = config("GET_USERDATA") # 유저 데이터 조회 api

st.title("지출 관리 시스템")

import streamlit as st

# Sidebar에서 페이지 선택
st.sidebar.title("SpendWise!")
page = st.sidebar.selectbox("항목 선택", ["데이터 입력", "데이터 분석", "Settings"])

# 페이지에 따라 다른 내용 표시
if page == "데이터 입력": # 지출 or 수입 데이터를 입력하는 페이지
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
        response = requests.post(DATA_CREATE, json=userdata)

        # 요청 결과 출력
        if response.status_code == 200:
            st.success("데이터가 성공적으로 저장되었습니다.")
            st.json(response.json())  # 저장된 데이터 출력
        else:
            st.error(f"오류 발생: {response.status_code}")
            st.write(response.text)

elif page == "데이터 분석": # 지출 or 수입 데이터 조회 페이지
        st.title("이번달 지출/수입 조회")
        transaction_type = st.selectbox("조회할 데이터",["지출/수입 선택","지출", "수입"])

        if transaction_type == "지출/수입 선택":
            response = requests.get(GET_USERDATA)
            
            if response.status_code == 200:
                data = response.json()
                st.write(data)
            else:
                st.error("데이터를 가져오지 못했습니다.")

        if transaction_type == "지출":
            # 여기서 백엔드 API 호출 (지출 내역 조회)
            response = requests.get(GET_USERDATA, params={"transaction_type": "지출"})
            if response.status_code == 200:
                data = response.json()  # API에서 받은 데이터
                st.write(data)  # 데이터를 화면에 출력
            else:
                st.error("데이터를 가져오지 못했습니다.")

        if transaction_type == "수입":

            response = requests.get(GET_USERDATA, params={"transaction_type": "수입"})
            if response.status_code == 200:
                data = response.json() # API에서 받은 데이터
                st.write(data)

elif page == "Settings": # 뭐할지 모르겠음
    st.title("Settings Page")
    st.write("This is the settings page. You can change your preferences here.")