from modules.api_list import UPDATE_USERDATA, GET_ALL_DATA, DELETE_DATA
from modules.utils import fetch_data
from datetime import datetime
import streamlit as st
import pandas as pd
import requests

def update_delete_userdata():
    # 초기 상태 변수 설정
    if "query_clicked" not in st.session_state:
        st.session_state.query_clicked = False
    if "query_params" not in st.session_state:
        st.session_state.query_params = {}
    if "fetched_data" not in st.session_state:
        st.session_state.fetched_data = pd.DataFrame()

    # 메인 화면에서 "데이터 조회" 버튼
    if st.button("데이터 조회", key="데이터/수정 삭제 데이터 조회 버튼",use_container_width=True, type="primary"):
        st.session_state.query_clicked = True

    # query_clicked 상태가 True일 때만 다이얼로그 표시
    if st.session_state.query_clicked:
        show_query_dialog()

    # 데이터가 조회되었을 때만 테이블 표시
    if not st.session_state.fetched_data.empty:
        show_data_table()


@st.dialog("조회")
def show_query_dialog():
    # 현재 연도, 월
    current_year = datetime.now().year
    current_month = datetime.now().month

    # 연도, 월 선택
    year = st.selectbox("년도", list(range(current_year, current_year - 10, -1)), index=0, key="수정/삭제 년도 선택")
    month = st.selectbox("월", list(range(1, 13)), index=current_month-1, key="수정/삭제 월 선택")

    # 거래 유형 선택 (지출/소득)
    # 요구사항: 다이얼로그 안에서 지출과 소득 선택 가능한 버튼
    # 여기서는 토글(radio)로 구현
    transaction_type = st.radio("거래 유형 선택", ["지출", "소득"])

    if st.button("조회하기", key="데이터 수정/삭제 전용 다이얼로그 버튼"):
        # 조회 파라미터 구성
        params = {
            "year": year,
            "month": month,
            "transaction_type": transaction_type
        }

        # 데이터 가져오기
        data = fetch_data(GET_ALL_DATA, params=params)
        df = pd.DataFrame(data)

        # 날짜 내림차순 정렬
        if not df.empty and "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date", ascending=False)

        st.session_state.fetched_data = df
        st.session_state.query_params = params
        st.session_state.query_clicked = False
        st.rerun()  # 다이얼로그 닫고 메인 화면 갱신

def show_data_table():
    df = st.session_state.fetched_data
    transaction_type = st.session_state.query_params.get("transaction_type", "지출")

    st.subheader(f"{transaction_type} 데이터")

    # 데이터 표시 및 수정/삭제 UI
    for row in df.itertuples():
        with st.expander(f"{row.date.strftime('%Y-%m-%d')} - {row.description} - {row.description_detail} - {row.amount:,}원"):
            with st.form(key=f"form_{row.id}"):
                # 기존 값으로 폼 초기화
                # description이 기존 리스트에 없을 경우 index 에러 처리 필요 -> try/except
                desc_options = ["식비", "교통비", "쇼핑", "기타", "송금"]
                try:
                    desc_index = desc_options.index(row.description)
                except ValueError:
                    desc_index = 0

                description = st.selectbox("내역", desc_options, index=desc_index, key=f"description_{row.id}")
                description_detail = st.text_input("상세 내역", value=row.description_detail, key=f"description_detail_{row.id}")
                amount = st.number_input("금액", value=row.amount, min_value=0, key=f"amount_{row.id}")
                date = st.date_input("날짜", value=row.date.date(), key=f"date_{row.id}")

                submit_button, delete_button = st.columns(2)
                with submit_button:
                    if st.form_submit_button(label="데이터 수정", use_container_width=True, type="secondary"):
                        updated_data = {
                            "transaction_type": transaction_type,
                            "description": description,
                            "description_detail": description_detail,
                            "amount": amount,
                            "date": str(date),
                        }
                        response = requests.put(UPDATE_USERDATA, params={"id": row.id}, json=updated_data)
                        if response.status_code == 200:
                            st.success("수정이 완료되었습니다.")
                            # 수정 후 데이터 재조회
                            refresh_data()
                        else:
                            st.error(f"수정 실패: {response.status_code}")

                with delete_button:
                    if st.form_submit_button(label="데이터 삭제", use_container_width=True, type="primary"):
                        delete_response = requests.delete(DELETE_DATA, params={"id": row.id})
                        if delete_response.status_code == 200:
                            st.success("데이터가 제거되었습니다.")
                            # 삭제 후 데이터 재조회
                            refresh_data()
                        else:
                            st.error(f"제거 실패: {delete_response.status_code}")


def refresh_data():
    # 데이터 다시 fetch
    params = st.session_state.query_params
    data = fetch_data(GET_ALL_DATA, params=params)
    df = pd.DataFrame(data)
    if not df.empty and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date", ascending=False)
    st.session_state.fetched_data = df
    st.rerun()