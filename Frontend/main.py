from modules.annual_analsis import get_annual_data
from modules.data_analysis import data_analysis_page
from modules.data_entry import data_entry_page
import streamlit as st

st.markdown("# Spend Wise!")

# 각 페이지에 해당하는 탭 생성
tab1, tab2, tab3 = st.tabs(["데이터 입력", "월간 데이터 조회", "연간 데이터 조회"])

# 각 탭별로 페이지 내용 표시
with tab1:
    data_entry_page()

with tab2:
    data_analysis_page()

with tab3:
    get_annual_data()