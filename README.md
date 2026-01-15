# 📊 투자 포트폴리오 대시보드

> **실시간 ETF 모니터링 & 포트폴리오 관리 웹 대시보드**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.52.2-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Personal-green.svg)](LICENSE)

개인 투자 포트폴리오를 실시간으로 모니터링하고 관리하는 Streamlit 기반 웹 대시보드입니다.

## 🎯 프로젝트 목표

이 프로젝트는 **개인 투자자를 위한 올인원 포트폴리오 관리 도구**를 목표로 합니다:

- **실시간 모니터링**: ISA 계좌와 미국 직투 계좌의 ETF/주식을 한눈에 파악
- **효율적인 정보 수집**: 여러 증권사 앱을 오가지 않고 한 곳에서 모든 정보 확인
- **데이터 기반 투자**: HOT 종목 추적, 배당률 비교, 포트폴리오 비중 관리
- **투자 전략 실행**: 목표 비중 설정, 리밸런싱 제안, 배당 캘린더 (예정)
- **학습과 성장**: Python/Streamlit 기술 스택을 활용한 실전 프로젝트

---

## ✨ 주요 기능

### 📈 실시간 모니터링
- **ISA 계좌**: 국내 상장 미국 배당 ETF 5종 실시간 가격 추적
- **미국 직투**: JEPI, JEPQ, SCHD, VYM 등 미국 ETF 실시간 가격 + 배당률
- **HOT 종목 Top 10**: 상승률 기준 인기 종목 (일일/주간/월간)
- **환율 정보**: USD/KRW 실시간 환율

### 🔍 종목 검색
- 티커 코드 (AAPL, 005930) 또는 한글 종목명 (삼성전자, 커버드콜)
- 한글/숫자/영문 자동 인식
- 여러 종목 발견 시 선택 가능한 UI

### 📋 워치리스트 관리
- 세션 기반 임시 워치리스트
- 목표 비중 설정 후 CSV 영구 저장
- HOT 종목에서 클릭 한 번으로 추가

---

## 🚀 빠른 시작

```bash
# 1. 프로젝트 디렉토리로 이동
cd investment-dashboard

# 2. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 앱 실행
cd src
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 자동 실행됩니다.

---

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| **Frontend** | Streamlit 1.52.2 |
| **Backend** | Python 3.12 |
| **Data API** | yfinance (미국 주식), FinanceDataReader (한국 주식) |
| **Data Processing** | pandas 2.3.3 |
| **Visualization** | plotly 6.5.0 (예정) |
| **Storage** | CSV |

---

## 📁 프로젝트 구조

```
investment-dashboard/
├── README.md                      # 프로젝트 소개
├── PROJECT_STATUS.md              # 현재 상태
├── requirements.txt               # Python 패키지
├── docs/
│   ├── screenshots/               # 스크린샷
│   ├── ISA_ETF_LIST.md           # ISA ETF 상세 정보
│   ├── US_DIRECT_ETF_LIST.md     # 미국 ETF 상세 정보
│   ├── INVESTMENT_STRATEGY.md    # 투자 전략
│   └── DEVELOPMENT_LOG.md        # 개발 일지
├── src/
│   ├── app.py                    # 메인 Streamlit 앱
│   ├── config.py                 # 설정값
│   ├── data_fetcher.py           # 데이터 수집
│   └── utils.py                  # 유틸리티
└── data/
    ├── isa_watchlist.csv         # ISA 관심 종목
    └── direct_watchlist.csv      # 미국 직투 관심 종목
```

---

## 📚 문서

- [프로젝트 현황](PROJECT_STATUS.md)
- [투자 전략](docs/INVESTMENT_STRATEGY.md)
- [개발 일지](docs/DEVELOPMENT_LOG.md)
- [ISA ETF 목록](docs/ISA_ETF_LIST.md)
- [미국 ETF 목록](docs/US_DIRECT_ETF_LIST.md)

---

## 🎯 로드맵

| 버전 | 상태 | 주요 기능 |
|------|------|----------|
| v0.1 | ✅ 완료 | ISA/미국 직투 탭, 실시간 가격 조회 |
| v0.2 | ✅ 완료 | HOT 종목 Top 10, 종목 검색, 임시 워치리스트 |
| v0.3 | 🔄 진행 예정 | 종목별 차트, 포트폴리오 비중 차트 |
| v0.4 | 📋 계획 중 | 보유 수량 입력, 평가액 계산, 수익률 |
| v0.5 | 📋 계획 중 | 배당 캘린더, 월별 배당 수익 |

자세한 로드맵은 [PROJECT_STATUS.md](PROJECT_STATUS.md)를 참고하세요.

---

## 💡 사용 팁

### 종목 검색
- **미국 주식**: `AAPL`, `SCHD` 등
- **한국 주식**: `005930` (삼성전자), `448330` (삼성전자우)
- **한글 검색**: `삼성전자`, `커버드콜` (부분 매칭 지원)

### 워치리스트
1. HOT 종목 탭에서 관심 종목 찾기
2. ➕ 버튼으로 임시 워치리스트에 추가
3. 각 탭에서 임시 종목 확인
4. 목표 비중 설정 후 CSV에 영구 저장

---

## 📝 참고사항

- 이 대시보드는 **투자 참고용**이며, 투자 결정은 본인 책임입니다
- 실시간 데이터는 약간의 지연이 있을 수 있습니다
- 임시 워치리스트는 세션 종료 시 사라집니다

---

## 👨‍💻 개발자

DevOps/SRE 엔지니어의 개인 프로젝트

---

**버전**: v0.2 | **마지막 업데이트**: 2026-01-15

