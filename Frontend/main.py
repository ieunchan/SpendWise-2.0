import streamlit as st
from modules.data_entry import data_entry_page
from modules.data_analysis import data_analysis_page

st.markdown("# Spend Wise!")

# 각 페이지에 해당하는 탭 생성
tab1, tab2 = st.tabs(["데이터 입력", "데이터 분석"])

# 각 탭별로 페이지 내용 표시
with tab1:
    data_entry_page()

with tab2:
    data_analysis_page()
