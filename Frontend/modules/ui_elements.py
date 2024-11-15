import plotly.express as px
import streamlit as st
import pandas as pd

def display_selectbox(options, label="선택"):
    """Streamlit selectbox 생성 함수"""
    return st.selectbox(label, options)

def display_expense_pie_chart(data, title="지출 차트"):
    """Plotly 원형 그래프 표시"""
    custom_colors = ["#8B0000", "#800000", "#660000", "#4B0000", "#330000"]
    fig = px.pie(data, names="description", values="total_amount", title=title, hole=0.3)
    fig.update_traces(
        text=[f"{desc}: {amt:,}원" for desc, amt in zip(data["description"], data["total_amount"])],
        textinfo="text",
        hovertemplate="%{label}: %{value:,}원<extra></extra>",
        marker=dict(colors=custom_colors),
        pull=[0.2] * len(data)
    )
    st.plotly_chart(fig)

def display_income_pie_chart(data, title="소득 그래프"):
    """Plotly 원형 그래프 표시 - 소득 전용"""
    custom_colors = ["#1E90FF", "#4169E1", "#00BFFF", "#87CEFA", "#4682B4"]
    fig = px.pie(data, names="내역", values="금액", title=title, hole=0.3)
    fig.update_traces(
        text=[f"{desc}: {amt:,}원" for desc, amt in zip(data["내역"], data["금액"])],
        textinfo="text",
        hovertemplate="%{label}: %{value:,}원<extra></extra>",
        marker=dict(colors=custom_colors),
        pull=[0.02] * len(data)  # 조각 간격 조정
    )
    st.plotly_chart(fig)