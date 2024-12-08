from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd

# 지출 부분 파이차트
def display_expense_pie_chart(data, title="지출 차트"):
    """Plotly 원형 그래프 표시"""
    custom_colors = ["#E53935", "#F44336", "#FF5252", "#FF6E6E", "#FF8A80"]
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

    custom_colors = ["#1E90FF", "#4169E1", "#00BFFF", "#87CEFA", "#4682B4"]
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


    # 요청 보낸 시간 기록
    request_time = datetime.now()
    st.write(f"📤 요청 보낸 시간: {request_time.strftime('%Y-%m-%d %H:%M:%S')}")

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
        color_discrete_map = {"지출": "#C62828", "소득": "#1E3A8A"}  # 진한 색상 지정
    )

    # 그래프 레이아웃 설정
    fig.update_traces(texttemplate='%{text:,}원', textposition="auto", textfont=dict(size=22, color="#F7E8C7"))  # 텍스트 표시 형식
    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(1, 13)),  # x축 눈금: 1월~12월
            ticktext=[f"{i}월" for i in range(1, 13)],
        ),
        yaxis=dict(tickformat=",", title="금액 (원)"),
        legend_title="거래 유형",
        height=500,  # 그래프 높이
    )

    # Streamlit에 그래프 표시
    st.plotly_chart(fig)

    # 완료 시간 기록
    completion_time = datetime.now()
    st.write(f"✅ 완료 시간: {completion_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 소요 시간 계산
    elapsed_time = (completion_time - request_time).total_seconds()
    st.write(f"⏱ 소요 시간: {elapsed_time:.2f}초")


# Spend Wise! 아스키 아트
def spendwise():
    st.markdown("""
<style>
@keyframes color-change {
  0% { background-position: 0% 50%; }  /* 왼쪽에서 시작 */
  100% { background-position: 100% 50%; } /* 오른쪽으로 이동 */
}


.rainbow-text {
  font-family: 'Courier New', monospace;
  font-size: 18px;
  font-weight: bold;
  background: linear-gradient(90deg, #F7E8C7, #333333); /* 진한 파랑 → 부드러운 검정 */
  background-size: 35%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: color-change 10s linear infinite; /* 일정 속도로 이동 */
  line-height: 1.1 ;
  white-space: pre;
  margin-top: -70px;
  margin-bottom: 100px;
  padding: -100px;
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
                                                          

</div>
""", unsafe_allow_html=True)

