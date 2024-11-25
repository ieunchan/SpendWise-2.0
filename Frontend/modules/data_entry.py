from decouple import AutoConfig
from datetime import date
import asyncio
import streamlit as st
import requests

config = AutoConfig()
DATA_CREATE = config("DATA_CREATE")

def data_entry_page():
    st.header("데이터를 입력하세요")
    
    # 거래 유형 선택
    transaction_type = st.selectbox("거래 유형", ["지출", "소득"])

    # 거래 유형에 따라 다른 입력 요소 표시
    if transaction_type == "지출":
        description = st.selectbox("내역", ["식비", "교통비", "쇼핑", "기타"])
        description_detail = st.text_input("상세 내역 설명을 입력하세요")
    else:
        description = st.text_input("소득 내역")
        description_detail = description

    # 나머지 입력 필드
    amount = st.number_input("금액", min_value=0)
    st.write(f"입력한 금액: {amount:,} 원")
    date_input = st.date_input("날짜", value=date.today())
    

    # 모든 필드가 입력되었는지 확인
    is_valid = (
        transaction_type
        and description
        and (description_detail if transaction_type == "지출" else True)
        and amount > 0
        and date_input
    )

    # 모든 필드가 채워져야만 데이터 전송
    submit_button, reset_button = st.columns(2)

    with submit_button:
        if st.button("데이터 전송", key='데이터 입력 탭 데이터 제출 버튼', use_container_width=True, type='primary'):
            if is_valid:
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
            else:
                st.error("모든 필드가 올바르게 입력되어야 제출할 수 있습니다.")
    with reset_button:
        if st.button('초기화', key="데이터 입력탭 초기화 버튼", use_container_width=True, type='secondary'):
            st.rerun()