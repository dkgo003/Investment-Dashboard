# 개발 일지

---

## 2026-01-06 (월) - 프로젝트 시작

### 📋 작업 내용

#### 프로젝트 초기화
- [x] 프로젝트 폴더 구조 생성
  - `docs/`, `src/`, `data/` 디렉토리 생성
- [x] `requirements.txt` 작성
  - Streamlit, yfinance, FinanceDataReader, pandas, plotly, APScheduler 추가
- [x] `.gitignore` 생성
  - Python, 가상환경, IDE, OS 관련 파일 제외
- [x] `README.md` 작성
  - 프로젝트 개요, 설치 방법, 실행 방법 작성

#### 문서 작성
- [x] `docs/ISA_ETF_LIST.md` 작성
  - 국내 상장 미국 배당 ETF 5종 상세 분석
  - 포트폴리오 추천안 3가지
  - 리밸런싱 전략 및 체크리스트
- [x] `docs/US_DIRECT_ETF_LIST.md` 작성
  - 미국 직투 배당 ETF 4종 (JEPI, JEPQ, SCHD, VYM) 상세 분석
  - 포트폴리오 추천안 3가지
  - 세금 계산 예시 및 절세 전략
- [x] `docs/INVESTMENT_STRATEGY.md` 작성
  - 단기/중기/장기 투자 목표
  - 2026년 초기 투자 계획 (ISA 2,000만원, 직투 500만원)
  - 연도별 추가 투자 계획
  - 리스크 관리 및 배당금 활용 전략
  - 예상 성과 시뮬레이션 (보수적/적극적)
- [x] `docs/DEVELOPMENT_LOG.md` 작성 (이 문서)

### 🎯 다음 할 일

#### Step 3: CSV 데이터 파일 생성
- [ ] `data/isa_watchlist.csv` 생성
  - ISA 관심 종목 5개 (종목코드, 이름, 타입, 목표비중)
- [ ] `data/direct_watchlist.csv` 생성
  - 직투 관심 종목 4개 (티커, 이름, 타입, 목표비중)

#### Step 4: Streamlit 앱 개발
- [ ] `src/config.py` 생성
  - 설정값 관리 (업데이트 주기, API 관련 설정 등)
- [ ] `src/data_fetcher.py` 생성
  - yfinance로 미국 ETF 데이터 가져오기
  - FinanceDataReader로 한국 ETF 데이터 가져오기
  - 에러 핸들링 포함
- [ ] `src/utils.py` 생성
  - 유틸리티 함수들 (데이터 포맷팅, 계산 등)
- [ ] `src/app.py` 생성
  - ISA 탭 / 직투 탭 기본 구조
  - CSV 파일에서 관심 종목 로드
  - 각 종목별 실시간 가격 표시
  - 배당률, 등락률 표시
  - 목표 비중 vs 현재 비중 표시

#### Step 5: 개발 환경 설정
- [ ] 가상환경 생성 및 패키지 설치
- [ ] Git 초기화 (선택사항)
- [ ] 첫 실행 테스트

### 💡 아이디어 및 메모

#### 기술적 고려사항
1. **데이터 캐싱**
   - Streamlit의 `@st.cache_data` 사용
   - API 호출 횟수 제한 대비
   - 캐시 유효 시간: 5분 정도?

2. **에러 핸들링**
   - API 호출 실패 시 재시도 로직
   - 네트워크 오류 시 사용자 친화적 메시지
   - 종목 코드 오류 시 예외 처리

3. **UI/UX**
   - 탭으로 ISA/직투 분리
   - 카드 형식으로 각 ETF 정보 표시
   - 상승: 초록색, 하락: 빨간색
   - 모바일 반응형 고려

4. **데이터 갱신**
   - 자동 새로고침 옵션 추가?
   - 수동 새로고침 버튼
   - 마지막 업데이트 시간 표시

#### 향후 개선 아이디어
- [ ] 포트폴리오 입력 기능 (보유 수량, 평균 단가)
- [ ] 실제 수익률 계산
- [ ] 배당금 캘린더 (배당락일, 배당 지급일)
- [ ] 리밸런싱 추천 기능
- [ ] 금융 뉴스 크롤링
- [ ] 차트 및 그래프 추가 (가격 추이, 배당 추이)
- [ ] 환율 정보 표시
- [ ] 알림 기능 (목표가 도달, 배당락일 등)

### 📚 학습 내용

#### Streamlit 기본 개념
- `st.tabs()`: 탭 UI 생성
- `st.metric()`: 지표 표시 (가격, 등락률 등)
- `st.dataframe()`: 테이블 표시
- `st.cache_data()`: 데이터 캐싱

#### FinanceDataReader 사용법
- 한국 ETF 데이터 조회
- 종목 코드로 현재가, 등락률 조회

#### yfinance 사용법
- 미국 ETF 데이터 조회
- 티커로 현재가, 배당률 조회

### 🐛 문제 및 해결

#### 문제 1: 한국 ETF 데이터 소스
- **문제**: 한국 상장 ETF 실시간 가격을 어떻게 가져올까?
- **해결**: FinanceDataReader 라이브러리 사용
  - KRX (한국거래소) 데이터 지원
  - 종목 코드로 조회 가능
  - 예시: `fdr.DataReader('479920')`

#### 문제 2: CSV 파일 구조
- **문제**: CSV에 어떤 컬럼을 포함해야 할까?
- **해결**: 최소한의 정보로 시작
  - `ticker`: 종목코드/티커
  - `name`: 종목명
  - `type`: ETF 타입 (커버드콜, 전통 배당 등)
  - `target_ratio`: 목표 비중 (%)
  - 추후 `current_shares`, `avg_price` 등 추가 가능

### 🎓 참고 자료

- [Streamlit 공식 문서](https://docs.streamlit.io)
- [yfinance GitHub](https://github.com/ranaroussi/yfinance)
- [FinanceDataReader 문서](https://github.com/FinanceData/FinanceDataReader)
- [Plotly 문서](https://plotly.com/python/)

### ⏰ 소요 시간

- 프로젝트 구조 설계: 30분
- 문서 작성 (ISA, 직투, 전략, 개발일지): 2시간
- 다음 단계 계획: 30분
- **총 소요 시간**: 약 3시간

---

## 2026-01-06 (월) - 오후: MVP 완성 및 버그 수정

### 📋 작업 내용

#### Step 3-5: 전체 앱 구현 완료 ✅
- [x] CSV 데이터 파일 생성
  - `data/isa_watchlist.csv` - ISA 관심 종목 5개
  - `data/direct_watchlist.csv` - 미국 직투 관심 종목 4개
- [x] `src/config.py` 작성
  - 캐시 TTL, 세금, 색상, 환율 등 설정값 관리
- [x] `src/utils.py` 작성
  - 포맷팅 함수 (가격, 퍼센트, 비율 등)
  - 계산 함수 (환전, 세후 배당금 등)
- [x] `src/data_fetcher.py` 작성
  - yfinance로 미국 ETF 데이터 수집
  - FinanceDataReader로 한국 ETF 데이터 수집
  - 환율 조회 기능
  - 에러 핸들링 및 재시도 로직
- [x] `src/app.py` 작성
  - Streamlit 메인 앱
  - ISA 탭, 미국 직투 탭, 전체 요약 탭
  - 실시간 데이터 표시 (현재가, 등락률, 배당률)
  - 사이드바 (환율, 새로고침 버튼)
- [x] 가상환경 생성 및 패키지 설치
- [x] 첫 실행 성공

### 🐛 문제 해결

#### 문제 1: DataFrame 포맷팅 에러
- **문제**: `TypeError: unsupported format string passed to NoneType.__format__`
- **원인**: 데이터프레임의 `None` 값을 포맷팅할 때 에러 발생
- **해결**: 포맷팅 함수에서 `None` 체크 후 "N/A" 반환
  ```python
  def format_price_safe(val):
      if val is None or pd.isna(val):
          return "N/A"
      return f"{val:,.0f}"
  ```

#### 문제 2: 미국 ETF 배당률 1000% 표시
- **문제**: JEPI 배당률이 815%, SCHD가 374%로 잘못 표시
- **원인**: yfinance가 이미 퍼센트 형태로 제공 (8.15 = 8.15%)하는데 코드에서 100을 곱함
- **해결**: 100 곱하는 코드 제거
  ```python
  # 수정 전
  dividend_yield = info.get('dividendYield')
  if dividend_yield:
      dividend_yield = dividend_yield * 100  # ❌

  # 수정 후
  dividend_yield = info.get('dividendYield')  # ✅ 그대로 사용
  if dividend_yield is None:
      dividend_yield = 0
  ```

#### 문제 3: 한국 ETF 종목코드 오류
- **문제**: CSV에 입력된 종목코드(479920, 481580 등)가 실제로 존재하지 않음
- **해결**: FinanceDataReader로 실제 ETF 목록 조회 후 정확한 코드로 교체
  | 기존 (잘못) | 수정 후 | 종목명 |
  |---------|--------|--------|
  | 479920 | 441640 | KODEX 미국배당커버드콜액티브 |
  | 481580 | 402970 | ACE 미국배당다우존스 |
  | 458730 | 458730 | TIGER 미국배당다우존스 (유지) |
  | 458750 | 458760 | TIGER 미국배당다우존스타겟커버드콜2호 |
  | 371460 | 474220 | TIGER 미국테크TOP10타겟커버드콜 |

#### 문제 4: 한국 ETF 데이터 조회 실패 - "'int' object is not iterable"
- **문제**: 모든 한국 ETF에서 "데이터를 불러올 수 없습니다" 표시
- **원인**: CSV에서 `ticker` 컬럼이 정수(int64)로 읽혔는데, FinanceDataReader는 문자열을 기대
- **해결**: `enrich_watchlist_with_data` 함수에서 ticker를 문자열로 변환
  ```python
  ticker = str(row['ticker'])  # 문자열로 변환
  ```

### ✅ 최종 결과

#### 작동하는 기능
- ✅ ISA 탭: 한국 ETF 5종 실시간 가격 표시
- ✅ 미국 직투 탭: 미국 ETF 4종 실시간 가격 + 배당률 표시
- ✅ 전체 요약 탭: 통합 포트폴리오 뷰
- ✅ 사이드바: USD/KRW 환율, 데이터 새로고침
- ✅ 에러 핸들링: None 값 처리, API 실패 시 재시도
- ✅ 캐시: 5분 TTL로 API 호출 최소화

#### 확인된 데이터 (2026-01-06 기준)
**한국 ETF:**
- KODEX 미국배당커버드콜액티브: 12,780원 (+0.91%)
- ACE 미국배당다우존스: 13,115원 (+0.38%)
- TIGER 미국배당다우존스: 12,910원 (+0.43%)
- TIGER 미국배당다우존스타겟커버드콜2호: 9,965원 (+0.05%)
- TIGER 미국테크TOP10타겟커버드콜: 15,840원 (+0.13%)

**미국 ETF:**
- JEPI: $57.47 (+0.26%, 배당률 8.15%)
- JEPQ: $58.44 (+0.60%, 배당률 10.13%)
- SCHD: $27.91 (+0.65%, 배당률 3.74%)
- VYM: $145.82 (+0.73%, 배당률 2.42%)

### 🎓 학습 내용

#### yfinance API 이해
- `dividendYield`는 이미 퍼센트 형태로 제공 (0.0815가 아니라 8.15)
- `currentPrice` vs `regularMarketPrice` 차이 이해
- `info` 딕셔너리에서 None 값 처리 중요

#### FinanceDataReader 활용
- `StockListing('ETF/KR')`: 한국 ETF 전체 목록 조회 가능
- 컬럼명이 `Code`가 아니라 `Symbol`
- `DataReader(ticker, start='2024-01-01')`: 과거 데이터 조회
- Ticker는 반드시 문자열로 전달

#### Pandas 데이터 타입 주의
- CSV에서 숫자로 된 문자열은 자동으로 int64로 변환됨
- `str()` 변환 필요
- `pd.isna()` vs `is None` 차이 이해

#### Streamlit 캐싱
- `@st.cache_data(ttl=300)`: 5분 캐시
- 파일 변경 시 자동 재실행 (개발 모드)
- `st.cache_data.clear()`: 수동 캐시 클리어

### 💡 개선 아이디어

#### 단기 개선 사항
- [ ] 한국 ETF 배당률 수동 입력 (FinanceDataReader는 배당률 미제공)
- [ ] 로딩 스피너 개선
- [ ] 에러 메시지 한글화
- [ ] 차트 추가 (가격 추이)

#### 중기 개선 사항
- [ ] 실제 보유 수량 입력 기능
- [ ] 포트폴리오 평가액 계산
- [ ] 리밸런싱 추천 기능
- [ ] 배당 캘린더

### 🔧 기술 스택 정리

**Frontend**: Streamlit 1.52.2
**Data APIs**:
- yfinance 1.0 (미국 주식)
- finance-datareader 0.9.101 (한국 주식)
**Data Processing**: pandas 2.3.3
**Visualization**: plotly 6.5.0 (아직 미사용)
**Environment**: Python 3.12, Ubuntu (WSL2)

### ⏰ 소요 시간

- Step 3-5 구현: 2시간
- 버그 수정 (4건): 1.5시간
- 테스트 및 검증: 30분
- **총 소요 시간**: 약 4시간

### 🎯 다음 할 일

#### 우선순위 1: 데이터 개선
- [ ] 한국 ETF 배당률 정보 추가 (CSV 또는 수동 입력)
- [ ] 환율 API 안정성 개선

#### 우선순위 2: 기능 추가
- [ ] 포트폴리오 입력 기능 (보유 수량, 평균 단가)
- [ ] 총 평가액 및 수익률 계산
- [ ] 월 예상 배당금 계산

#### 우선순위 3: UI/UX 개선
- [ ] 차트 추가 (Plotly)
- [ ] 모바일 반응형 개선
- [ ] 다크모드 지원

### 📝 메모

#### 프로젝트 위치
- 프로젝트 저장소: `/home/iklee/investment-dashboard`

---

## 🚀 설치 및 실행 가이드

### 📦 Case 1: 가상환경이 이미 있는 경우 (빠른 실행)

**1단계: 프로젝트 폴더로 이동**
```bash
cd /home/iklee/investment-dashboard
```

**2단계: 가상환경 활성화**
```bash
source venv/bin/activate
```

**3단계: Streamlit 앱 실행**
```bash
cd src
streamlit run app.py
```

**접속 URL**
- 로컬: http://localhost:8501
- 네트워크: http://172.23.67.51:8501 (같은 WiFi 내)

**종료 방법**
- 터미널에서 `Ctrl + C`

**가상환경 비활성화 (앱 종료 후)**
```bash
deactivate
```

---

### 🔧 Case 2: 가상환경이 없는 경우 (처음 설치)

**1단계: 프로젝트 폴더로 이동**
```bash
cd /home/iklee/investment-dashboard
```

**2단계: Python 가상환경 생성**
```bash
python3 -m venv venv
```

**3단계: 가상환경 활성화**
```bash
source venv/bin/activate
```

**4단계: 필수 패키지 설치**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

설치되는 패키지:
- `streamlit` - 웹 대시보드 프레임워크
- `yfinance` - 미국 주식 데이터 API
- `finance-datareader` - 한국 주식 데이터 API
- `pandas` - 데이터 처리
- `plotly` - 차트 라이브러리
- `APScheduler` - 스케줄링
- `python-dotenv` - 환경변수 관리

**5단계: Streamlit 앱 실행**
```bash
cd src
streamlit run app.py
```

처음 실행 시 이메일 입력 화면이 나오면 **Enter 키**를 눌러 건너뛰세요.

**접속 URL**
- 로컬: http://localhost:8501
- 네트워크: http://172.23.67.51:8501 (같은 WiFi 내)

---

### 🔄 백그라운드 실행 (선택사항)

터미널을 닫아도 계속 실행되게 하려면:

```bash
cd /home/iklee/investment-dashboard/src
source ../venv/bin/activate
streamlit run app.py --server.headless=true --server.port=8501 &
```

백그라운드 프로세스 확인:
```bash
ps aux | grep streamlit
```

백그라운드 프로세스 종료:
```bash
# 프로세스 ID 확인 후
kill [프로세스ID]
```

---

### 🐛 트러블슈팅

**문제: `venv/bin/activate` 파일이 없다고 나옴**
- 해결: 가상환경을 다시 생성하세요 (`python3 -m venv venv`)

**문제: `ModuleNotFoundError: No module named 'streamlit'`**
- 해결: 가상환경 활성화 후 패키지를 다시 설치하세요 (`pip install -r requirements.txt`)

**문제: 한국 ETF 데이터가 안 나옴**
- 해결: 한국 증시 시간(09:00-15:30) 이후에는 전일 종가가 표시됩니다 (정상)

**문제: 미국 ETF 데이터가 안 나옴**
- 해결: 미국 증시 개장 전이거나 주말일 경우 전일 종가가 표시됩니다 (정상)

**문제: 환율이 기본값(1320)으로 표시됨**
- 해결: API 호출 실패 시 기본값 사용 (사이드바 새로고침 버튼 클릭)

---

## 2026-01-15 (수) - HOT 종목 & 검색 기능 추가

### 📋 작업 내용

#### HOT 종목 Top 10 탭 구현
- [x] 미국 S&P 500 주요 종목 상승률 Top 10 표시
- [x] 한국 ETF 상승률 Top 10 표시
- [x] 기간 선택 기능 (일일/주간/월간)
- [x] 클릭으로 임시 워치리스트 추가 기능
- [x] `fetch_hot_us_stocks()` 함수 구현
- [x] `fetch_hot_kr_etfs()` 함수 구현

#### 종목 검색 기능 구현
- [x] 사이드바에 검색창 추가
- [x] 미국 주식 티커 검색 (AAPL, SCHD 등)
- [x] 한국 주식/ETF 티커 검색 (005930, 448330 등)
- [x] 한국 종목명 검색 (삼성전자, 커버드콜 등)
- [x] 한글 검색 시 부분 매칭으로 최대 10개 결과 표시
- [x] 여러 결과 발견 시 expander UI로 선택 가능
- [x] `search_stock_multiple()` 함수 구현

#### 임시 워치리스트 시스템
- [x] 세션 기반 임시 워치리스트 구현
- [x] ISA/미국 직투 별도 관리
- [x] HOT 종목 탭에서 추가 기능
- [x] 검색 결과에서 추가 기능
- [x] 각 탭에서 임시 종목 확인 및 삭제
- [x] 영구 저장 기능 (목표 비중 입력 후 CSV 추가)

### 🐛 문제 해결

#### 문제 1: 한국 ETF 컬럼명 이슈
- **문제**: `❌ HOT 한국 ETF 데이터 가져오기 실패: 'Code'`
- **원인**: FinanceDataReader ETF 리스트의 컬럼명이 일관적이지 않음
- **해결**: 동적 컬럼명 감지 로직 추가
  ```python
  code_col = 'Code' if 'Code' in etf_list.columns else 'Symbol' if 'Symbol' in etf_list.columns else None
  name_col = 'Name' if 'Name' in etf_list.columns else None
  ```

#### 문제 2: 배당률 None 값 에러
- **문제**: `TypeError: unsupported format string passed to NoneType.__format__`
- **원인**: 배당률이 None일 때 포맷팅 시도
- **해결**: 조건문 수정 `if div_yield is not None and div_yield > 0:`

#### 문제 3: use_container_width 경고
- **문제**: Streamlit deprecation 경고 발생
- **해결**: `use_container_width=True` → `width='stretch'`로 5곳 수정

#### 문제 4: 한국어 검색어가 yfinance로 전송
- **문제**: "커버드콜" 검색 시 HTTP 404 에러 (yfinance API)
- **원인**: 검색 우선순위가 미국 주식 우선이었음
- **해결**: 한글 검색어는 바로 한국 ETF 검색으로 라우팅

#### 문제 5: 005930 (삼성전자) 검색 실패
- **문제**: 숫자 티커를 yfinance로 보내서 404 에러
- **원인**: 숫자로만 된 티커를 미국 주식으로 인식
- **해결**: `query.isdigit()` 체크로 한국 주식 우선 검색

### ✅ 최종 결과

#### 작동하는 기능
- ✅ HOT 종목 Top 10 탭 (미국/한국 분리)
- ✅ 기간별 상승률 필터 (일일/주간/월간)
- ✅ 종목 검색 (티커/한글 이름)
- ✅ 다중 검색 결과 expander UI
- ✅ 임시 워치리스트 추가/삭제
- ✅ CSV 영구 저장 (목표 비중 포함)
- ✅ 005930 (삼성전자) 검색 지원
- ✅ 한글 종목명 부분 매칭 검색

#### 검색 로직 우선순위
1. **한글 포함** → 한국 ETF 리스트에서 종목명 검색 (최대 10개)
2. **숫자만** → 한국 주식/ETF 티커 검색 (005930 등)
3. **영문 포함** → 미국 주식 티커 검색 (AAPL 등)

### 🎓 학습 내용

#### Streamlit 세션 상태
- `st.session_state`로 임시 데이터 관리
- 세션별로 독립적인 워치리스트 유지
- 새로고침 시 초기화됨 (임시 특성)

#### FinanceDataReader 활용
- `StockListing('ETF/KR')`: 전체 ETF 목록 조회
- `StockListing('KRX')`: 전체 주식 목록 조회
- 종목명 조회로 005930 → 삼성전자 변환 가능
- 컬럼명이 API 버전에 따라 다를 수 있음 (동적 감지 필요)

#### yfinance 성능 최적화
- S&P 500 전체 조회는 너무 느림
- 주요 50개 종목만 조회로 속도 개선
- 기간별 수익률 계산 (`1d`, `5d`, `1mo`)

#### Python 문자열 검사
- `query.isdigit()`: 숫자만으로 구성됐는지 확인
- `'\uac00' <= char <= '\ud7a3'`: 한글 유니코드 범위 체크
- `str.contains()`: Pandas 문자열 부분 매칭

### 💡 개선 아이디어

#### 구현 완료
- ✅ 임시 → 영구 저장 하이브리드 시스템
- ✅ 한글 종목명 검색
- ✅ 다중 검색 결과 UI
- ✅ 005930 같은 숫자 티커 지원

#### 향후 개선 사항
- [ ] HOT 종목 캐시 시간 조정 (현재 5분)
- [ ] 검색 히스토리 기능
- [ ] 즐겨찾기 기능
- [ ] 한국 주식도 HOT 종목에 포함

### 🔧 주요 코드 변경

**data_fetcher.py:**
- `fetch_hot_us_stocks()` 추가: S&P 500 주요 50개 종목 상승률 Top 10
- `fetch_hot_kr_etfs()` 추가: 한국 ETF 50개 상승률 Top 10
- `search_stock_multiple()` 추가: 다중 검색 결과 반환
- `fetch_kr_etf_data()` 수정: KRX 리스트에서 종목명 자동 조회
- 검색 우선순위 재정렬: 한글 → 숫자 → 영문

**app.py:**
- HOT 종목 Top 10 탭 추가 (4번째 탭)
- 사이드바 검색 UI 추가
- 임시 워치리스트 섹션 추가 (ISA/미국 직투)
- 영구 저장 UI (expander + 목표 비중 입력)
- `width='stretch'` 업데이트 (5곳)

### ⏰ 소요 시간

- HOT 종목 기능 구현: 1.5시간
- 검색 기능 구현: 1시간
- 임시 워치리스트 시스템: 1시간
- 버그 수정 (5건): 1.5시간
- **총 소요 시간**: 약 5시간

### 🎯 다음 할 일

#### 우선순위 1: 시각화
- [ ] 종목별 가격 차트 추가
- [ ] 포트폴리오 비중 파이 차트
- [ ] 수익률 추이 그래프

#### 우선순위 2: 포트폴리오 관리
- [ ] 보유 수량 입력 기능
- [ ] 평가액 계산
- [ ] 총 수익률 계산
- [ ] 리밸런싱 제안

#### 우선순위 3: 배당 관리
- [ ] 배당 캘린더
- [ ] 월별 예상 배당 수익
- [ ] 배당 성장률 분석

### 📝 메모

#### 성능 최적화 팁
- HOT 종목은 50개만 조회 (200개 → 50개로 감소)
- 5분 캐시로 API 호출 최소화
- 검색은 실시간 (캐시 없음)

#### 사용자 경험 개선
- 삼성전자우 vs 삼성전자 구분 명확히 표시
- 여러 결과 있을 때 expander로 선택 편의성 향상
- 임시 워치리스트로 실험 가능

---

## Template for Future Entries

```markdown
## YYYY-MM-DD (요일) - 작업 제목

### 📋 작업 내용
- [ ] 작업 항목 1
- [ ] 작업 항목 2

### 🐛 문제 해결
**문제**:
**해결**:

### 💡 아이디어 및 메모


### 🎓 학습 내용


### ⏰ 소요 시간


### 🎯 다음 할 일

```

---

> 개발 일지 작성 팁:
> 1. 작업 시작 전에 TODO 리스트 작성
> 2. 작업 완료 후 체크 표시
> 3. 문제 발생 시 즉시 기록
> 4. 학습한 내용 간단히 정리
> 5. 다음 작업 계획 미리 작성
