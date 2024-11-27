from datetime import datetime
from typing import Optional

# 계속 사용할 수 있는 함수를 모아둡니다.

def get_month_range(year: int, month: int, day: Optional[int] = None):
    start_of_month = datetime(year, month, 1)
    if month == 12:
        end_of_month = datetime(year + 1, 1, 1)
    else:
        end_of_month = datetime(year, month + 1, 1)
    return start_of_month, end_of_month