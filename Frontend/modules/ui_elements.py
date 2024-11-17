import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def display_selectbox(options, label="선택"):
    """Streamlit selectbox 생성 함수"""
    return st.selectbox(label, options)


# 지출 부분 파이차트
def display_expense_pie_chart(data, title="지출 차트"):
    """Plotly 원형 그래프 표시"""
    custom_colors = ["#5E2021", "#4682B4", "#9ACD32", "#768BAA", "#FF8C33"]
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


def display_expense_line_graph(data, title="월별 지출 총액"):
    """월별 지출 꺾은선 그래프 표시"""
    
    # 데이터를 DataFrame으로 변환 (data는 리스트 형식으로 가정)
    df = pd.DataFrame(data)
    
    # y축 최대값 설정 (최대값의 약 1.2배로 여유를 둠)
    max_y = int(df["total_amount"].max() * 1.5)
    
    # 꺾은선 그래프 생성
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["month"],
        y=df["total_amount"],
        mode="lines+markers+text",
        name="월별 지출 합계",
        line=dict(color="indianred", width=5),
        marker=dict(color="indianred", size=15),
        text=[f"{v:,}원" for v in df["total_amount"]],  # 점 위에 표시할 텍스트
        textposition="top center",  # 텍스트 위치 (점 위 중앙)
        hovertemplate='%{x}월: %{y:,}원'  # 툴팁 포맷 설정
    ))

    # 그래프 레이아웃 설정
    fig.update_layout(
        title=title,
        xaxis_title="월",
        yaxis_title="지출 총액 (원)",
        xaxis=dict(tickmode="linear", dtick=1),  # 월 단위 눈금
        yaxis=dict(range=[0, max_y], tickformat=",.0f"),  # y축을 쉼표 있는 원 단위로 설정
        template="plotly_white"
    )

    # Streamlit을 사용해 그래프 표시
    st.plotly_chart(fig)


def display_income_line_graph(data, title="월별 소득 총액"):
    """월별 소득 꺾은선 그래프 표시"""
    
    # 데이터를 DataFrame으로 변환 (data는 리스트 형식으로 가정)
    df = pd.DataFrame(data)
    
    # y축 최대값 설정 (최대값의 약 1.2배로 여유를 둠)
    max_y = int(df["total_amount"].max() * 1.5)
    
    # 꺾은선 그래프 생성
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["month"],
        y=df["total_amount"],
        mode="lines+markers+text",
        name="월별 소득 합계",
        line=dict(color="indianred", width=5),
        marker=dict(color="indianred", size=15),
        text=[f"{v:,}원" for v in df["total_amount"]],  # 점 위에 표시할 텍스트
        textposition="top center",  # 텍스트 위치 (점 위 중앙)
        hovertemplate='%{x}월: %{y:,}원'  # 툴팁 포맷 설정
    ))

    # 그래프 레이아웃 설정
    fig.update_layout(
        title=title,
        xaxis_title="월",
        yaxis_title="소득 총액 (원)",
        xaxis=dict(tickmode="linear", dtick=1),  # 월 단위 눈금
        yaxis=dict(range=[0, max_y], tickformat=",.0f"),  # y축을 쉼표 있는 원 단위로 설정
        template="plotly_white"
    )

    # Streamlit을 사용해 그래프 표시
    st.plotly_chart(fig)