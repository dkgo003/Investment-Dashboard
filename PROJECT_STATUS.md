# 📊 투자 대시보드 - 프로젝트 현황

> 마지막 업데이트: 2026-01-06
> 버전: v0.1 (MVP)

---

## ✅ 현재 상태: MVP 완성

### 작동하는 기능

- ✅ **ISA 계좌 탭**: 한국 상장 ETF 5종 실시간 모니터링
- ✅ **미국 직투 탭**: 미국 상장 ETF 4종 실시간 모니터링 + 배당률
- ✅ **전체 요약 탭**: 통합 포트폴리오 뷰
- ✅ **사이드바**: USD/KRW 환율, 새로고침 버튼
- ✅ **데이터 캐싱**: 5분 TTL (API 호출 최소화)
- ✅ **에러 핸들링**: None 값 처리, API 실패 시 재시도

### 모니터링 중인 종목

**ISA (한국 상장 ETF) - 5종목**
1. KODEX 미국배당커버드콜액티브 (441640)
2. ACE 미국배당다우존스 (402970)
3. TIGER 미국배당다우존스 (458730)
4. TIGER 미국배당다우존스타겟커버드콜2호 (458760)
5. TIGER 미국테크TOP10타겟커버드콜 (474220)

**미국 직투 - 4종목**
1. JEPI - JPMorgan Equity Premium Income
2. JEPQ - JPMorgan Nasdaq Equity Premium Income
3. SCHD - Schwab US Dividend Equity
4. VYM - Vanguard High Dividend Yield

---

## 🔧 기술 스택

- **Frontend**: Streamlit 1.52.2
- **Backend**: Python 3.12
- **Data APIs**:
  - yfinance 1.0 (미국 주식)
  - finance-datareader 0.9.101 (한국 주식)
- **Data Processing**: pandas 2.3.3
- **Visualization**: plotly 6.5.0 (설치됨, 아직 미사용)
- **Environment**: Ubuntu (WSL2)

---

## 📂 파일 구조

```
investment-dashboard/
├── README.md                   # 프로젝트 소개
├── PROJECT_STATUS.md           # 이 파일 (프로젝트 현황)
├── requirements.txt            # Python 패키지 목록
├── .gitignore
├── docs/
│   ├── ISA_ETF_LIST.md        # ISA ETF 상세 정보
│   ├── US_DIRECT_ETF_LIST.md  # 미국 ETF 상세 정보
│   ├── INVESTMENT_STRATEGY.md # 투자 전략
│   └── DEVELOPMENT_LOG.md     # 개발 일지 ⭐ 중요
├── src/
│   ├── app.py                 # 메인 Streamlit 앱
│   ├── config.py              # 설정값 (캐시, 세금, 환율 등)
│   ├── data_fetcher.py        # 데이터 수집 (yfinance, FinanceDataReader)
│   └── utils.py               # 유틸리티 함수 (포맷팅, 계산)
└── data/
    ├── isa_watchlist.csv      # ISA 관심 종목 목록
    └── direct_watchlist.csv   # 직투 관심 종목 목록
```

---

## 🚀 빠른 시작

### 1. 가상환경 활성화
```bash
cd investment-dashboard
source venv/bin/activate
```

### 2. 앱 실행
```bash
cd src
streamlit run app.py
```

### 3. 브라우저 접속
- **로컬**: http://localhost:8501
- **네트워크**: http://172.23.67.51:8501 (같은 WiFi 내)

---

## 🐛 알려진 이슈

### 현재 제한사항
1. **한국 ETF 배당률**: FinanceDataReader가 배당률을 제공하지 않아 표시 안 됨
   - 해결 방법: CSV에 수동으로 추가 예정
2. **한국 ETF 종목명**: 일부 종목은 종목코드만 표시됨
   - 해결 방법: CSV의 name 컬럼 활용

### 해결된 이슈 (2026-01-06)
- ✅ DataFrame 포맷팅 에러 (None 값 처리)
- ✅ 미국 ETF 배당률 1000% 표시 오류
- ✅ 한국 ETF 종목코드 오류
- ✅ CSV ticker int64 타입 이슈

---

## 📋 다음 단계 (우선순위)

### 🔴 우선순위 1: 데이터 개선
- [ ] 한국 ETF 배당률 정보 추가
- [ ] 환율 API 안정성 개선

### 🟡 우선순위 2: 핵심 기능
- [ ] 포트폴리오 입력 기능 (보유 수량, 평균 단가)
- [ ] 총 평가액 및 수익률 계산
- [ ] 월 예상 배당금 계산

### 🟢 우선순위 3: UI/UX
- [ ] 차트 추가 (Plotly)
- [ ] 모바일 반응형 개선
- [ ] 다크모드 지원

---

## 📚 참고 문서

### 내부 문서
- **개발 일지**: [DEVELOPMENT_LOG.md](docs/DEVELOPMENT_LOG.md) ⭐ **여기에 모든 업데이트 기록**
- **투자 전략**: [INVESTMENT_STRATEGY.md](docs/INVESTMENT_STRATEGY.md)
- **ISA ETF 정보**: [ISA_ETF_LIST.md](docs/ISA_ETF_LIST.md)
- **미국 ETF 정보**: [US_DIRECT_ETF_LIST.md](docs/US_DIRECT_ETF_LIST.md)

### 외부 자료
- [Streamlit 공식 문서](https://docs.streamlit.io)
- [yfinance GitHub](https://github.com/ranaroussi/yfinance)
- [FinanceDataReader 문서](https://github.com/FinanceData/FinanceDataReader)

---

## 💡 주요 학습 포인트

### yfinance API
- `dividendYield`는 이미 퍼센트 (8.15 = 8.15%, 0.0815 아님)
- `info` 딕셔너리에서 None 값 처리 필수

### FinanceDataReader
- `StockListing('ETF/KR')`: 한국 ETF 목록 조회
- Ticker는 반드시 **문자열**로 전달 (CSV에서 int로 읽힐 수 있음)

### Streamlit
- `@st.cache_data(ttl=300)`: 5분 캐시
- 파일 변경 감지 자동 재실행

### Pandas
- CSV에서 숫자 컬럼은 자동으로 int64 변환 → `str()` 필요

---

## 🔔 트러블슈팅

### 앱이 실행 안 됨
```bash
# 가상환경 활성화 확인
source venv/bin/activate

# 패키지 재설치
pip install -r requirements.txt
```

### 데이터가 표시 안 됨
- 사이드바 "🔄 데이터 새로고침" 버튼 클릭
- 또는 브라우저 새로고침 (Ctrl+Shift+R)

### 한국 증시 시간 외에는?
- FinanceDataReader는 가장 최근 거래일 종가 표시
- 실시간이 아니므로 정상

---

## 📞 연락처

- 개발자: DevOps/SRE 엔지니어
- 프로젝트: 개인 투자 관리 대시보드

---

## 📝 버전 히스토리

| 버전 | 날짜 | 주요 변경사항 |
|------|------|--------------|
| v0.1 | 2026-01-06 | MVP 완성, ISA/직투 탭, 실시간 가격 조회 |

---

> **중요**: 모든 개발 내역은 [DEVELOPMENT_LOG.md](docs/DEVELOPMENT_LOG.md)에 기록됩니다.
> 새로운 Claude Code 세션에서는 해당 파일을 먼저 확인하세요!
