from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd

# 지출 부분 파이차트
def display_expense_pie_chart(data, title="지출 차트"):
    """Plotly 원형 그래프 표시"""
    custom_colors = ["#B71C1C", "#D32F2F", "#E53935", "#F44336", "#FF5252", "#C62828"]
    fig = px.pie(data, names="description", values="total_amount", title=title, hole=0.3)
    fig.update_traces(
        text=[f"{desc}: {amt:,}원" for desc, amt in zip(data["description"], data["total_amount"])],
        textinfo="text",
        hovertemplate="%{label}: %{value:,}원<extra></extra>",
        marker=dict(colors=custom_colors),
        pull=[0.09] * len(data)
    )
    st.plotly_chart(fig)


# 소득 부분 파이차트
def display_income_pie_chart(data, title="소득 차트"):
    """원형 그래프 표시 - 소득 전용"""

    if data is None or len(data) == 0:  # data가 None이거나 비어있는 경우
        st.warning("표시할 데이터가 없습니다.")
        return  # 함수 종료

    custom_colors = ["#228B22", "#2E8B57", "#6B8E23", "#556B2F", "#3A5F0B", "#4E9258", "#2F4F2F"]
    fig = px.pie(data, names="내역", values="금액", title=title, hole=0.3)
    fig.update_traces(
        text=[f"{desc}: {amt:,}원" for desc, amt in zip(data["내역"], data["금액"])],
        textinfo="text",
        textposition="auto",
        hovertemplate="%{label}: %{value:,}원<extra></extra>",
        marker=dict(colors=custom_colors),
        pull=[0.09] * len(data)  # 조각 간격 조정
    )
    st.plotly_chart(fig)


def display_combined_bar_chart(data, title="월별 소득 및 지출"):
    """월별 소득 및 지출 누적 막대 그래프 표시"""

    # 데이터를 Stacked Bar Chart 형태로 변환
    expense_data = data[data["transaction_type"] == '지출']
    income_data = data[data["transaction_type"] == '소득']

    # 데이터 병합
    combined_data = pd.concat([expense_data, income_data])

    combined_data["formatted_amount"] = combined_data["total_amount"].apply(lambda x: f"{x:,}")

    # 막대그래프 생성
    fig = px.bar(
        combined_data,
        x="month",  # x축: 월
        y=f"total_amount",  # y축: 총 금액
        color="transaction_type",  # 색상 기준: 소득/지출
        barmode="group",  # 누적 막대그래프 설정
        labels={"total_amount": "금액 (원)", "month": "월", "transaction_type": "거래 유형"},
        title=title,
        text="total_amount", # 막대그래프에 표시할 텍스트
        color_discrete_map = {"지출": "#C62828", "소득": "#3B62B5"},  # 진한 색상 지정
        custom_data=["transaction_type"]

    )

    # 그래프 레이아웃 설정
    fig.update_traces(
        texttemplate='%{text:,}원', 
        textposition="auto", 
        textfont=dict(size=16, color="#F7E8C7"),
        hovertemplate="<b>거래 유형</b>: %{customdata[0]}<br>"
                    "<b>월</b>: %{x}<br>"
                    "<b>금액 (원)</b>: %{y:,.0f}원<br>"  # 금액에 천 단위 콤마 추가
        )  
    # 텍스트 표시 형식
    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(1, 13)),  # x축 눈금: 1월~12월
            ticktext=[f"{i}월" for i in range(1, 13)],
        ),
        yaxis=dict(
            range=[0, combined_data["total_amount"].max() * 1],  # y축 범위 조정
            tickformat=",", 
            title="금액 (원)"
        ),
        legend_title="거래 유형",
        height=500,  # 그래프 높이
    )

    # Streamlit에 그래프 표시
    st.plotly_chart(fig)

# Spend Wise! 아스키 아트
def spendwise():
    st.markdown("""
<style>
@keyframes color-fade {
  0% { color: #F7E8C7; }  /* 시작 색 */
  50% { color: #000000; } /* 중간 색 */
  100% { color: #F7E8C7; } /* 끝 색 */
}

.rainbow-text {
  font-family: 'Courier New', monospace;
  font-size: 18px;
  font-weight: bold;
  animation: color-fade 7s linear infinite; /* 색상이 점차 바뀌도록 설정 */
  line-height: 1.1;
  white-space: pre; /* 공백과 줄바꿈 유지 */
  margin-top: -70px;
  margin-bottom: 100px;
  padding: 20px;
}


</style>
<div class="rainbow-text">
     _____                                    __        __      __                             __     
    /\  _ `\                                 /\ \      /\ \  __/\ \    __                     /\ \    
    \ \,\S\_\    _____      __      ___      \_\ \     \ \ \/\ \ \ \  /\_\      ____     __   \ \ \   
     \/_\__ \   /\ '__`\  /'__`\  /' _ `\    /'_` \     \ \ \ \ \ \ \ \/\ \    /',__\  /'__`\  \ \ \  
       /\ \S\ \ \ \ \_\ \/\  __/  /\ \/\ \  /\ \_\ \     \ \ \_/ \_\ \ \ \ \  /\__, `\/\  __/   \ \_\ 
       \ `\____\ \ \ ,__/\ \____\ \ \_\ \_\ \ \___,_\     \ `\___x___/  \ \_\ \/\____/\ \____\   \/\_\ \
        
        \/_____/  \ \ \/  \/____/  \/_/\/_/  \/__,_ /      '\/__//__/    \/_/  \/___/  \/____/    \/_/
                   \ \_\                                                                                                          
                    \/_/                                                                                                          
                                                            
""", unsafe_allow_html=True)

