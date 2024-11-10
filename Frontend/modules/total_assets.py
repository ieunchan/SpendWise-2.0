import streamlit as st
from modules.api_list import GET_TOTAL_ASSETS
from modules.utils import fetch_data
from datetime import datetime

# CSS 스타일을 추가하여 탭 폰트 크기 조정
st.markdown(
    "<style> div.stTabs > div > div > button {font-size: 20px !important;  /* 폰트 크기를 조정 */}</style>",
    unsafe_allow_html=True
)

def total_asset_expend_income(key):
    # 데이터를 fetch_data를 통해 가져옴
    total_assets = fetch_data(GET_TOTAL_ASSETS)
    # 반환값 예시: [{"총 자산": total_assets, "총 수입": total_income, "총 지출": total_expend}]
    
    # 리스트 형태와 해당 key가 있는지 확인
    if total_assets and isinstance(total_assets, list) and key in total_assets[0]:
        # 첫 번째 항목에서 key 값에 해당하는 항목 가져오기
        total_data = total_assets[0].get(key)
        st.write(f"### {key}: {total_data:,}")  # 세 자리마다 콤마 추가
    else:
        st.write(f"{key} 데이터를 불러오지 못했습니다.")
    # total_asset_expend_income("총 자산")
    # total_asset_expend_income("총 수입")
    # total_asset_expend_income("총 지출")

def get_annual_data():
    type_input, year_input = st.columns(2)

    with type_input:
        transaction_type = st.tabs(["수입","지출"])
        

    with year_input:
        current_year = datetime.now().year
        year = st.selectbox("년도", list(range(current_year - 10, current_year + 1)), index=10, key="annual_select")

