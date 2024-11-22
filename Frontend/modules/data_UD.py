from modules.api_list import UPDATE_USERDATA, GET_ALL_DATA
from datetime import datetime
from modules.utils import fetch_data
import streamlit as st
import pandas as pd
import requests

def update_delete_userdata():
    # 상태 변수 초기화
    if "update_data_fetched" not in st.session_state:
        st.session_state.update_data_fetched = False
    if "update_show_data" not in st.session_state:
        st.session_state.update_show_data = False
    if "update_params" not in st.session_state:
        st.session_state.update_params = {}

    # 입력 필드: 거래 유형, 연도, 월
    type_input, year_input, month_input = st.columns(3)

    with type_input:
        transaction_type = st.radio("조회할 데이터를 입력하세요", ["지출", "소득"])

    with year_input:
        current_year = datetime.now().year
        year = st.selectbox("년도", list(range(current_year - 10, current_year + 1)), index=10, key="UD year input")

    with month_input:
        current_month = datetime.now().month
        month = st.selectbox("월", list(range(1, 13)), index=current_month - 1, key="UD month input")

    # 데이터 조회 버튼
    if st.button("데이터 조회", key="data for update/delete"):
        st.session_state.update_data_fetched = True
        st.session_state.update_params = {"year": year, "month": month, "transaction_type": transaction_type}
        st.session_state.update_show_data = True  # 데이터 표시 플래그

    # 데이터 조회 및 편집 UI 표시
    if st.session_state.update_data_fetched:
        params = st.session_state.update_params
        show_all_data_with_edit(params, transaction_type)


def show_all_data_with_edit(params, transaction_type):
    # API로 데이터 가져오기
    data = fetch_data(GET_ALL_DATA, params=params)
    df = pd.DataFrame(data)

    if not df.empty:
        st.subheader(f"{transaction_type} 데이터")

        # 데이터 표시 및 수정 UI 생성
        for idx, row in df.iterrows():
            with st.expander(f"날짜: {row['date']} -- 거래 유형: {row['description']} -- 상세내역: {row['description_detail']} -- 금액: {row['amount']:,}"):
                with st.form(key=f"form_{row['id']}"):
                    # 입력 필드
                    description = st.text_input("내역(식비, 교통비, 쇼핑, 기타)", value=row["description"], key=f"description_{row['id']}")
                    description_detail = st.text_input(
                        "상세 내역", value=row["description_detail"], key=f"description_detail_{row['id']}"
                    )
                    amount = st.number_input("금액", value=row["amount"], min_value=0, key=f"amount_{row['id']}")
                    date = st.date_input("날짜", value=pd.to_datetime(row["date"]).date(), key=f"date_{row['id']}")

                    # 저장 버튼
                    submit_button = st.form_submit_button(label="저장")
                    if submit_button:
                        # 수정 데이터 생성
                        updated_data = {
                            "transaction_type": transaction_type,
                            "description": description,
                            "description_detail": description_detail,
                            "amount": amount,
                            "date": str(date),
                        }

                        # API 호출
                        response = requests.put(
                            UPDATE_USERDATA, params={"id": row["id"]}, json=updated_data
                        )
                        if response.status_code == 200:
                            st.success("수정이 완료되었습니다.")
                        else:
                            st.error(f"수정 실패: {response.status_code}")
    else:
        st.warning("조회된 데이터가 없습니다.")