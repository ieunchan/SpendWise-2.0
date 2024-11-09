import streamlit as st
import requests
from decouple import AutoConfig
from datetime import datetime
import plotly.express as px
import pandas as pd



config = AutoConfig()
GET_USERDATA_EXPENSE = config("GET_USERDATA_EXPENSE")
GET_USERDATA_INCOME = config("GET_USERDATA_INCOME")
GET_EXPENSE_RANKING = config("GET_EXPENSE_RANKING")
GET_EXPENSE_DETAILS = config("GET_EXPENSE_DETAILS")

def data_analysis_page():
    type_input, year_input, month_input = st.columns(3)

    with type_input:
        transaction_type = st.selectbox("조회할 데이터", ["지출", "수입"])

    with year_input:
        current_year = datetime.now().year
        year = st.selectbox("년도", list(range(current_year - 10, current_year + 1)), index=10) # 올해부터 10전 전까지의 년도를 표시합니다.

    with month_input:
        current_month = datetime.now().month
        month = st.selectbox("월", list(range(1, 13)), index=current_month - 1) # 1월부터 12월까지를 표시합니다

    # 데이터 조회 요청 버튼
    if st.button("데이터 조회"):
        # 선택한 연도와 월을 쿼리 파라미터로 설정
        params = {"year": year, "month": month} # 데이터 조회 버튼을 누르면 생성되는 파라미터입니다.

        if transaction_type == "지출": # selectbox에서 '지출'을 선택했을 때의 로직
            # 지출 데이터 요청 및 처리
            expense_response = requests.get(GET_USERDATA_EXPENSE, params=params) # 이렇게하면 http://GET_USERDATA_EXPENSE/params 형식으로 백엔드에 전달됨
            if expense_response.status_code == 200:
                try:
                    expense_data = expense_response.json() 
                    
                    total_expense = sum(expense['amount'] for expense in expense_data) #json으로 파싱한 expense_data의 지출 액수의 총합을 구함
                    st.markdown(
                        f"<span style='color:#C74446; font-size:24px;'>{year}년 {month}월 지출 : {total_expense:,} 원</span>",
                        unsafe_allow_html=True) # 지출 금액 빨간색으로 하고 좀 더 크게 하기위해 html 사용
                except Exception as e:
                    st.error(f"지출 데이터 처리 중 오류 발생: {e}")
            else:
                st.error(f"지출 데이터 요청 오류: 상태 코드 {expense_response.status_code}")

            # 지출 랭킹 데이터 요청 및 처리
            expense_rank_response = requests.get(GET_EXPENSE_RANKING, params=params) # https://GET_EXPENSE_RANKING/params
            if expense_rank_response.status_code == 200:
                try:
                    rank_data = expense_rank_response.json()
                    st.markdown(f"### {year}년 {month}월 지출 내역별 랭킹")
                    for i, item in enumerate(rank_data, start=1): # i는 인덱스 번호이고 0부터가 아니고 1부터 시작
                        st.write(f"{i}. {item['description']}: {item['total_amount']:,} 원") # 인덱스 번호. 아이템 형식으로 순위가 매겨짐
                except Exception as e:
                    st.error(f"랭킹 데이터 처리 중 오류 발생: {e}")
            else:
                st.error(f"랭킹 데이터 요청 오류: 상태 코드 {expense_rank_response.status_code}")

            # 지출 내역 순위 조회
            response = requests.get(GET_EXPENSE_RANKING, params=params)
            if response.status_code == 200:
                expense_data = response.json()
                # JSON 데이터를 DataFrame으로 변환
                data = pd.DataFrame(expense_data)
                
                # Plotly 원형 그래프 생성
                rank_graph = px.pie(data, names="description", values="total_amount", title="그래프로 보기", hole=0.3) # 복잡한 그래프는 필요하지 않아서 plotly 사용.
                custom_colors = ["#5E2021", "#4682B4", "#9ACD32", "#768BAA", "#FF8C33"] # 그래프의 커스텀 색상
                rank_graph.update_traces(pull=[0.2] * len(data))
                # 퍼센트 대신 "카테고리: 금액" 형식으로 텍스트 표시
                rank_graph.update_traces(
                    text=[f"{description}: {amount:,}원" for description, amount in zip(data["description"], data["total_amount"])],
                    textinfo="text",
                    hovertemplate="%{label}: %{value:,}원<extra></extra>",
                    marker=dict(colors=custom_colors)  # 색상 리스트 적용
                )
                st.plotly_chart(rank_graph)
            else:
                st.error(f"지출 내역 순위 데이터를 가져오는 데 실패했습니다.")

        elif transaction_type == "수입":
            # 수입 데이터 요청 및 처리
            income_response = requests.get(GET_USERDATA_INCOME, params=params) # https://GET_USERDATA_INCOME/params
            if income_response.status_code == 200:
                try:
                    income_data = income_response.json()
                    total_income = sum(income['amount'] for income in income_data)
                    st.markdown(
                        f"<span style='color:#1E90FF; font-size:24px;'>{year}년 {month}월 수입 : {total_income:,} 원</span>",
                        unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"수입 데이터 처리 중 오류 발생: {e}")
            # 수입 내역 내림차순
            
            else:
                st.error(f"수입 데이터 요청 오류: 상태 코드 {income_response.status_code}")
