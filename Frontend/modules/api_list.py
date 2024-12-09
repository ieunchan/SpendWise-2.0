# from decouple import AutoConfig

# config = AutoConfig()

# DATA_CREATE = config("DATA_CREATE")
# GET_USERDATA_EXPENSE = config("GET_USERDATA_EXPENSE")
# GET_USERDATA_INCOME = config("GET_USERDATA_INCOME")
# GET_EXPENSE_RANKING = config("GET_EXPENSE_RANKING")
# GET_EXPENSE_DETAILS = config("GET_EXPENSE_DETAILS")
# GET_INCOME_RANKING = config("GET_INCOME_RANKING")
# GET_TOTAL_ASSETS = config("GET_TOTAL_ASSETS")
# GET_ANNUAL_EXPENSE_RANK = config("GET_ANNUAL_EXPENSE_RANK")
# GET_ANNUAL_INCOME_RANK = config("GET_ANNUAL_INCOME_RANK")
# UPDATE_USERDATA = config("UPDATE_USERDATA")
# GET_ALL_DATA = config("GET_ALL_DATA")
# DELETE_DATA = config("DELETE_DATA")
# GET_EXPENSE_INCOME_LINE_GRAPH_DATA = config("GET_EXPENSE_INCOME_LINE_GRAPH_DATA")


# api_list.py

# streamlit 배포용
import streamlit as st

# st.secrets로 API URL 가져오기
GET_EXPENSE_RANKING = st.secrets["api"]["GET_EXPENSE_RANKING"]
GET_EXPENSE_DETAILS = st.secrets["api"]["GET_EXPENSE_DETAILS"]
GET_ANNUAL_EXPENSE_RANK = st.secrets["api"]["GET_ANNUAL_EXPENSE_RANK"]
GET_USERDATA_EXPENSE = st.secrets["api"]["GET_USERDATA_EXPENSE"]

GET_USERDATA_INCOME = st.secrets["api"]["GET_USERDATA_INCOME"]
GET_INCOME_RANKING = st.secrets["api"]["GET_INCOME_RANKING"]
GET_ANNUAL_INCOME_RANK = st.secrets["api"]["GET_ANNUAL_INCOME_RANK"]

DATA_CREATE = st.secrets["api"]["DATA_CREATE"]
UPDATE_USERDATA = st.secrets["api"]["UPDATE_USERDATA"]
DELETE_DATA = st.secrets["api"]["DELETE_DATA"]

GET_TOTAL_ASSETS = st.secrets["api"]["GET_TOTAL_ASSETS"]
GET_ALL_DATA = st.secrets["api"]["GET_ALL_DATA"]
GET_EXPENSE_INCOME_LINE_GRAPH_DATA = st.secrets["api"]["GET_EXPENSE_INCOME_LINE_GRAPH_DATA"]