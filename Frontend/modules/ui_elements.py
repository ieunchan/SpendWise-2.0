import plotly.express as px
import streamlit as st
import pandas as pd

def display_selectbox(options, label="선택"):
    """Streamlit selectbox 생성 함수"""
    return st.selectbox(label, options)

def display_pie_chart(data, title="그래프로 보기"):
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