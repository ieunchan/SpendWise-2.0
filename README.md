 # *SpendWise! 2.0*
## *더 효율적인 수입/지출 관리 시스템*

# >>> SpendWise! 1.0 vs SpendWise! 2.0 비교 <<< #
---

| 비교 요소       | SpendWise-1.0                              | ***SpendWise-2.0***                            |
|----------------|-----------------------------------------|------------------------------------------|
| **데이터 저장** | CSV 파일                                | 데이터베이스 (SQLite)                     |
| **데이터 처리** | pandas로 CSV 처리, 입출력 병목 현상 발생         | SQLAlchemy ORM 기반 처리, 더 빠르고 효율적 |
| **시각화**      | Matplotlib (파일 저장 단계 포함)         | Plotly (간단한 그래프에는 더 효율적)       |
| **속도**       | CSV 읽기/쓰기에서 병목 현상 (약 1.5~2.4초) | 데이터베이스 기반 처리로 빠른 응답 (약 0.2~0.5초) |
| **확장성**      | 단일 사용자, 확장성 제한적               | 멀티유저, 클라우드 배포 가능              |
| **유지보수**    | 단일 파일, 모듈화 X                  | 모듈화 O                   |
| **반응성**      | 데이터 업데이트 시 페이지 전체 새로고침 필요 | 비동기로 더 높은 반응성 |
| **데이터 크기** | 대규모 데이터 처리에 비효율적            | 대규모 데이터 처리에도 안정적 성능         |
| **배포**        | 로컬 환경에서만 사용 가능                | 클라우드 배포 가능         |
---

# 주요 기능

 ## * 데이터 입력 탭
 ---
![spendwise 데이터 입력](https://github.com/user-attachments/assets/b737f381-82a0-43ee-bfd6-2b608b38fb16)
<hr>

  + 사용자가 수입/지출 데이터를 입력하면 DB에 저장이 되어야한다.
    
      + 유저 데이터:
          ```
          * 거래유형 : 수입/지출
          * 거래내역 : ex) 교통비(지출), 식비(지출), 월급(수입), 용돈(수입)
          * 상세내역 : 거래 내역에 대한 상세내역 기입. ex) 식비 -> 제육볶음
          * 금액 : 수입/지출에 대한 금액을 기입.
          * 날짜 : 수입/지출이 발생한 날짜를 기입.
          ```
    + '제출' 버튼 클릭 시, 모든 필드가 채워져 있으면 API를 통해 백엔드로 POST 요청
## * 월간 데이터 분석 탭
---
  ![월간 데이터 총합](https://github.com/user-attachments/assets/69bfa272-c78d-484c-ad72-e68976f950e2)
  <hr>

  +   사용자가 선택한 ***거래유형 - 년도 - 월*** 의 정보를 분석 후 시각화
  +   내역 별 지출 순위 표시
  +   각 내역 별 총 금액을 파이차트를 이용해 시각화
  +    파이차트의 각 부분은 내역 별 총 금액입니다.
  +   각 내역 별 상세 내역 조회 가능
## * 연간 데이터 분석 탭
---
![연간 데이터 조회](https://github.com/user-attachments/assets/5b804e3b-d77f-447d-bf5f-2be2bb63e9fb)
<hr>

+ 유저가 선택한 년도의 수입/지출 합계 확인 기능
+ 선택한 년도의 내역 별 지출 합계 확인 기능 => 파이차트
+ 선택한 년도의 1 ~ 12월의 지출 금액 꺾인 선 그래프로 시각화


## * 버전 기록:

+ 2.1: 총 자산 항상 화면에 표시 => 11/20 완료.
  + 사용자의 총 자산이 화면에 표시됨 => 완료
  + 총 자산은 (총 소득 - 총 지출)로 산출되어 표시됨. => 완료
+ 2.1.1: 도커 컴포즈 => 11/21일 완료
  +	프론트엔드와 백엔드의 도커 컴포즈 통합: Docker Compose를 사용해 Streamlit 프론트엔드와 FastAPI 백엔드를 동시에 실행하도록 구성. => 11/21 완료.
  +	도커 실행 명령어:   ```docker-compose up --build```
+ 2.2(예정): 저장된 데이터 수정, 삭제 기능(예정)
   + 데이터 수정 기능 => 11/22일 완료
      + ![수정 기능 추가](https://github.com/user-attachments/assets/15cd27cb-8b9e-479c-b473-c6a892e37e1f)

     
   + 데이터 삭제 기능(예정)

# 기술 스택 (Tech Stack)

## ⚙️ 백엔드 (Backend)
<p align="left">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white"> 
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=SQLite&logoColor=white">
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=SQLAlchemy&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=Pydantic&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white">
  <img src="https://img.shields.io/badge/.ENV-ECD53F?style=for-the-badge&logo=.ENV&logoColor=white">
  <img src="https://raw.githubusercontent.com/encode/uvicorn/master/docs/uvicorn.png" alt="Uvicorn" height="50">
</p>

---

## 🖥️ 프론트엔드 (Frontend)
<p align="left">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=Plotly&logoColor=white">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=Pandas&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white">
  <img src="https://img.shields.io/badge/.ENV-ECD53F?style=for-the-badge&logo=.ENV&logoColor=white">
</p>

