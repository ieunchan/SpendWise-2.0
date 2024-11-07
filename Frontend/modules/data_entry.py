import streamlit as st
from datetime import date
import requests
from decouple import AutoConfig

config = AutoConfig()
DATA_CREATE = config("DATA_CREATE")

# 입력 필드를 초기화하는 함수
def reset_form():
    st.session_state["transaction_type"] = "지출"
    st.session_state["description"] = "식비"
    st.session_state["description_detail"] = ""
    st.session_state["amount"] = 0
    st.session_state["date_input"] = date.today()

# 페이지 처음 로드 시 상태 초기화
if "transaction_type" not in st.session_state:
    reset_form()

def data_entry_page():
    st.header("데이터를 입력하세요")
    
    # 거래 유형 선택
    transaction_type = st.selectbox("거래 유형", ["지출", "수입"])

    # 거래 유형에 따라 다른 입력 요소 표시
    if transaction_type == "지출":
        description = st.selectbox("내역", ["식비", "교통비", "쇼핑", "기타"])
        description_detail = st.text_input("상세 내역 설명을 입력하세요")
    else:
        description = st.text_input("수입 내역")
        description_detail = None

    # 나머지 입력 필드
    amount = st.number_input("금액", min_value=0)
    st.write(f"입력한 금액: {amount:,.0f} 원")
    date_input = st.date_input("날짜", value=date.today())
    
    # 제출 버튼
    submit_button, reset_button = st.columns(2)

    # 제출 버튼 클릭 시 데이터 전송
    if submit_button.button("제출", use_container_width=True):
        userdata = {
            "transaction_type": transaction_type,
            "description": description,
            "description_detail": description_detail,
            "amount": amount,
            "date": str(date_input)
        }

        # 백엔드로 데이터 전송
        response = requests.post(DATA_CREATE, json=userdata)
        if response.status_code == 200:
            st.success("데이터가 성공적으로 저장되었습니다.")
            st.json(response.json())
        else:
            st.error(f"오류 발생: {response.status_code}")
            st.write(response.text)
    if reset_button.button("초기화", use_container_width=True, on_click=reset_form()):
        st.rerun()