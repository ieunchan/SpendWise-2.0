from decouple import AutoConfig

config = AutoConfig()

DATA_CREATE = config("DATA_CREATE")
GET_USERDATA_ALL = config("GET_USERDATA_ALL")
GET_USERDATA_EXPENSE = config("GET_USERDATA_EXPENSE")
GET_USERDATA_INCOME = config("GET_USERDATA_INCOME")
GET_EXPENSE_RANKING = config("GET_EXPENSE_RANKING")
GET_EXPENSE_DETAILS = config("GET_EXPENSE_DETAILS")
GET_INCOME_RANKING = config("GET_INCOME_RANKING")
GET_TOTAL_ASSETS = config("GET_TOTAL_ASSETS")
GET_ANNUAL_EXPENSE_RANK = config("GET_ANNUAL_EXPENSE_RANK")
GET_ANNUAL_INCOME_RANK = config("GET_ANNUAL_INCOME_RANK")
GET_MONTHLY_EXPENSE_DATA = config("GET_MONTHLY_EXPENSE_DATA")
GET_MONTHLY_INCOME_DATA = config("GET_MONTHLY_INCOME_DATA")
UPDATE_USERDATA = config("UPDATE_USERDATA")
GET_ALL_DATA = config("GET_ALL_DATA")
