"""
설정 파일
투자 대시보드의 전역 설정값을 관리합니다.
"""

import os
from pathlib import Path

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent

# 데이터 파일 경로
DATA_DIR = PROJECT_ROOT / "data"
ISA_WATCHLIST_PATH = DATA_DIR / "isa_watchlist.csv"
DIRECT_WATCHLIST_PATH = DATA_DIR / "direct_watchlist.csv"

# API 설정
CACHE_TTL = 300  # 캐시 유효 시간 (초) - 5분
REQUEST_TIMEOUT = 10  # API 요청 타임아웃 (초)
MAX_RETRIES = 3  # API 요청 재시도 횟수

# 환율 설정 (기본값)
DEFAULT_USD_KRW = 1320  # 원/달러 기본 환율

# 세금 설정
US_WITHHOLDING_TAX = 0.15  # 미국 배당 원천징수세 15%
KR_DIVIDEND_TAX = 0.154  # 한국 배당소득세 15.4%
ISA_TAX_FREE_LIMIT = 2000000  # ISA 비과세 한도 (원)

# UI 설정
STREAMLIT_THEME = "light"
REFRESH_INTERVAL = 60  # 자동 새로고침 간격 (초) - 사용하지 않을 수도 있음

# 색상 설정
COLOR_POSITIVE = "#00C853"  # 상승 색상 (초록)
COLOR_NEGATIVE = "#D32F2F"  # 하락 색상 (빨강)
COLOR_NEUTRAL = "#757575"  # 중립 색상 (회색)

# 데이터 형식
DECIMAL_PLACES_PRICE = 2  # 가격 소수점 자리수
DECIMAL_PLACES_PERCENT = 2  # 퍼센트 소수점 자리수
DECIMAL_PLACES_RATIO = 1  # 비율 소수점 자리수
