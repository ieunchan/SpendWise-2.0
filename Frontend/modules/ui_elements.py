import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd

def display_selectbox(options, label="선택"):
    """Streamlit selectbox 생성 함수"""
    return st.selectbox(label, options)


# 지출 부분 파이차트
def display_expense_pie_chart(data, title="지출 차트"):
    """Plotly 원형 그래프 표시"""
    custom_colors = ["#5E2021", "#6F392A", "#4D3622", "#704C27", "#FF8C33"]
    fig = px.pie(data, names="description", values="total_amount", title=title, hole=0.3)
    fig.update_traces(
        text=[f"{desc}: {amt:,}원" for desc, amt in zip(data["description"], data["total_amount"])],
        textinfo="text",
        hovertemplate="%{label}: %{value:,}원<extra></extra>",
        marker=dict(colors=custom_colors),
        pull=[0.2] * len(data)
    )
    st.plotly_chart(fig)


# 소득 부분 파이차트
def display_income_pie_chart(data, title="소득 그래프"):
    """원형 그래프 표시 - 소득 전용"""
    custom_colors = ["#1E90FF", "#4169E1", "#00BFFF", "#87CEFA", "#4682B4"]
    fig = px.pie(data, names="내역", values="금액", title=title, hole=0.3)
    fig.update_traces(
        text=[f"{desc}: {amt:,}원" for desc, amt in zip(data["내역"], data["금액"])],
        textinfo="text",
        textposition="auto",
        hovertemplate="%{label}: %{value:,}원<extra></extra>",
        marker=dict(colors=custom_colors),
        pull=[0.02] * len(data)  # 조각 간격 조정
    )
    st.plotly_chart(fig)


def display_combined_bar_chart(data, title="월별 소득 및 지출"):
    """월별 소득 및 지출 누적 막대 그래프 표시"""

    # 데이터를 Stacked Bar Chart 형태로 변환
    expense_data = data[data["transaction_type"] == '지출']
    income_data = data[data["transaction_type"] == '소득']

    # 데이터 병합
    combined_data = pd.concat([expense_data, income_data])

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
        color_discrete_map={"지출": "#62090A", "소득": "#001A5C"}  # 색상 지정
    )

    # 그래프 레이아웃 설정
    fig.update_traces(texttemplate='%{text:,}원', textposition="inside", textfont=dict(size=22, color="#FFEEAA"),)  # 텍스트 표시 형식
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