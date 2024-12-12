from modules.api_list import DATA_CREATE
from datetime import date
import streamlit as st
import requests


def data_entry_page():
    # 초기 상태 설정
    if "transaction_type" not in st.session_state:
        st.session_state.transaction_type = "지출"
    if "description" not in st.session_state:
        st.session_state.description = ""
    if "description_detail" not in st.session_state:
        st.session_state.description_detail = ""
    if "amount" not in st.session_state:
        st.session_state.amount = 0
    if "date_input" not in st.session_state:
        st.session_state.date_input = date.today()
    
    # 거래 유형 선택
    st.session_state.transaction_type = st.selectbox(
        "거래 유형",
        ["지출", "소득"],
        index=0 if st.session_state.transaction_type == "지출" else 1
    )

    # 거래 유형에 따라 다른 입력 요소 표시
    if st.session_state.transaction_type == "지출":
        st.session_state.description = st.selectbox(
            "내역",
            ["식비", "교통비", "쇼핑", "기타", "송금"],
            index=0 if st.session_state.description == "" else
            ["식비", "교통비", "쇼핑", "기타", "송금"].index(st.session_state.description)
        )
        st.session_state.description_detail = st.text_input(
            "상세 내역 설명을 입력하세요",
            value=st.session_state.description_detail
        )
    else:
        st.session_state.description = st.text_input(
            "소득 내역",
            value=st.session_state.description
        )
        st.session_state.description_detail = st.session_state.description

    # 나머지 입력 필드
    st.session_state.amount = st.number_input(
        "금액",
        min_value=0,
        value=st.session_state.amount
    )
    st.write(f"입력한 금액: {st.session_state.amount:,} 원")
    st.session_state.date_input = st.date_input(
        "날짜",
        value=st.session_state.date_input
    )

    # 모든 필드가 입력되었는지 확인
    is_valid = (
        st.session_state.transaction_type
        and st.session_state.description
        and (
            st.session_state.description_detail
            if st.session_state.transaction_type == "지출"
            else True
        )
        and st.session_state.amount > 0
        and st.session_state.date_input
    )

    if st.button(
        "데이터 전송 (전송 후 한번 더 누르면 초기화됩니다.)",
        key="데이터 입력 탭 데이터 제출 버튼",
        use_container_width=True,
        type="primary"
    ):
        if is_valid:
            payload = {
                "transaction_type": st.session_state.transaction_type,
                "description": st.session_state.description,
                "description_detail": st.session_state.description_detail,
                "amount": st.session_state.amount,
                "date": str(st.session_state.date_input)
            }

            # 백엔드로 데이터 전송
            response = requests.post(DATA_CREATE, json=payload)
            if response.status_code == 200:
                st.success("데이터 전송이 완료되었습니다.")
                st.json(response.json())
                # 필드값 자동 초기화
                st.session_state.transaction_type = "지출"
                st.session_state.description = ""
                st.session_state.description_detail = ""
                st.session_state.amount = 0
                st.session_state.date_input = date.today()
            else:
                st.error(f"오류 발생: {response.status_code}")
                st.write(response.text)
        else:
            st.error("모든 필드가 올바르게 입력되어야 제출할 수 있습니다.")