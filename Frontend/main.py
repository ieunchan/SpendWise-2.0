from modules.annual_analsis import get_annual_data
from modules.data_analysis import data_analysis_page
from modules.data_entry import data_entry_page
from modules.api_list import GET_TOTAL_ASSETS
from modules.utils import fetch_data
import streamlit as st

st.markdown("# Spend Wise!")
data = fetch_data(GET_TOTAL_ASSETS)
# 숫자 값 추출
if data and isinstance(data, list) and "total_asset" in data[0]:
    total_amount = data[0]["total_asset"]
    st.markdown(f"### 총 자산: {total_amount:,}원")  # 원하는 형식으로 출력
else:
    st.write("데이터가 올바르지 않습니다.")
# 각 페이지에 해당하는 탭 생성
tab1, tab2, tab3 = st.tabs(["데이터 입력", "월간 데이터 조회", "연간 데이터 조회"])

# 각 탭별로 페이지 내용 표시
with tab1:
    data_entry_page()

with tab2:
    data_analysis_page()

with tab3:
    get_annual_data()