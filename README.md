# 📊 투자 대시보드 (Investment Dashboard)

개인 투자 포트폴리오를 한눈에 모니터링하는 Streamlit 기반 웹 대시보드입니다.

## 🎯 프로젝트 목표

- ISA 계좌와 미국 직투 계좌를 분리하여 관리
- 실시간 ETF 가격 및 배당률 모니터링
- 투자 전략 문서화 및 관리
- 포트폴리오 리밸런싱 지원

## 🚀 주요 기능

### 📈 ISA 계좌 모니터링
- 국내 상장 미국 배당 ETF 실시간 가격
- 목표 비중 vs 현재 비중 비교
- 배당률 추적

### 🌎 미국 직투 계좌 모니터링
- 미국 상장 배당 ETF (JEPI, JEPQ, SCHD, VYM 등)
- USD 기준 실시간 가격
- 포트폴리오 밸런스 확인

### 📰 금융 뉴스 큐레이션 (예정)
- 미국/한국 주요 금융 뉴스
- 아침 브리핑 형식

### 🔥 HOT 주식 정보 (예정)
- S&P 500 / 나스닥 상승률 TOP 5

## 📁 프로젝트 구조

```
investment-dashboard/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── ISA_ETF_LIST.md          # ISA 투자 가능 ETF 목록
│   ├── US_DIRECT_ETF_LIST.md    # 미국 직투 ETF 목록
│   ├── INVESTMENT_STRATEGY.md   # 투자 전략 문서
│   └── DEVELOPMENT_LOG.md       # 개발 일지
├── src/
│   ├── app.py                   # 메인 Streamlit 앱
│   ├── config.py                # 설정 파일
│   ├── data_fetcher.py          # 데이터 수집 모듈
│   └── utils.py                 # 유틸리티 함수
└── data/
    ├── isa_watchlist.csv        # ISA 관심 종목
    └── direct_watchlist.csv     # 직투 관심 종목
```

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Data API**:
  - yfinance (미국 주식)
  - FinanceDataReader (한국 주식)
- **Data Visualization**: Plotly
- **Data Storage**: CSV

## 📦 설치 방법

### 1. 저장소 클론
```bash
cd investment-dashboard
```

### 2. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

## 🚀 실행 방법

```bash
cd src
streamlit run app.py
```

브라우저에서 자동으로 `http://localhost:8501`이 열립니다.

## 📚 문서

- [ISA ETF 목록](docs/ISA_ETF_LIST.md)
- [미국 직투 ETF 목록](docs/US_DIRECT_ETF_LIST.md)
- [투자 전략](docs/INVESTMENT_STRATEGY.md)
- [개발 일지](docs/DEVELOPMENT_LOG.md)

## 🎯 개발 로드맵

### Phase 1: MVP ✅ 완료 (2026-01-06)
- [x] 프로젝트 구조 생성
- [x] 기본 문서 작성 (ISA, 직투, 투자전략, 개발일지)
- [x] ISA/직투 탭 기본 구조
- [x] 실시간 가격 조회 기능
- [x] 환율 정보 표시
- [x] 데이터 캐싱 (5분 TTL)

### Phase 2: 핵심 기능 (진행 예정)
- [ ] 포트폴리오 현황 대시보드
- [ ] 실제 보유 수량 입력 기능
- [ ] 배당금 계산기
- [ ] 리밸런싱 추천
- [ ] 한국 ETF 배당률 정보 추가

### Phase 3: 추가 기능
- [ ] 금융 뉴스 큐레이션
- [ ] HOT 주식 정보
- [ ] 차트 및 그래프 추가 (Plotly)
- [ ] 배당 캘린더
- [ ] 모바일 반응형 개선

## 👨‍💻 개발자

- DevOps/SRE 엔지니어
- Python 기반 개인 프로젝트

## 📄 라이선스

개인 프로젝트 (공개)

## 📝 참고사항

- 이 대시보드는 투자 참고용이며, 투자 결정은 본인 책임입니다.
- 실시간 데이터는 약간의 지연이 있을 수 있습니다.
- API 제한으로 인해 과도한 새로고침은 피해주세요.
