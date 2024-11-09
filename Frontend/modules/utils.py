import requests

def fetch_data(url, params=None):
    """API로부터 데이터를 가져오는 유틸리티 함수."""
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"API 요청 실패: 상태 코드 {response.status_code}")