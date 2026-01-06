"""
데이터 수집 모듈
yfinance와 FinanceDataReader를 사용하여 ETF 데이터를 가져옵니다.
"""

import yfinance as yf
import FinanceDataReader as fdr
import pandas as pd
from typing import Dict, Optional, Union
import time
import config


def fetch_us_etf_data(ticker: str, retries: int = config.MAX_RETRIES) -> Optional[Dict]:
    """
    미국 ETF 데이터를 yfinance로 가져옵니다.

    Args:
        ticker: ETF 티커 (예: "JEPI", "SCHD")
        retries: 재시도 횟수

    Returns:
        ETF 데이터 딕셔너리 또는 None (실패 시)
        {
            'ticker': str,
            'name': str,
            'price': float,
            'change': float,
            'change_percent': float,
            'dividend_yield': float,
            'currency': str
        }
    """
    for attempt in range(retries):
        try:
            # yfinance 티커 객체 생성
            stock = yf.Ticker(ticker)

            # 기본 정보 가져오기
            info = stock.info

            # 현재가
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            if current_price is None:
                # 최근 거래일 종가 사용
                hist = stock.history(period='1d')
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]

            # 전일 종가
            previous_close = info.get('previousClose') or info.get('regularMarketPreviousClose')

            # 등락액 및 등락률 계산
            if current_price and previous_close:
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100
            else:
                change = 0
                change_percent = 0

            # 배당률 (yfinance는 이미 퍼센트 형태로 제공: 8.15 = 8.15%)
            dividend_yield = info.get('dividendYield')
            if dividend_yield is None:
                dividend_yield = 0

            # 종목명
            name = info.get('longName') or info.get('shortName') or ticker

            return {
                'ticker': ticker,
                'name': name,
                'price': current_price,
                'change': change,
                'change_percent': change_percent,
                'dividend_yield': dividend_yield,
                'currency': 'USD'
            }

        except Exception as e:
            print(f"⚠️ {ticker} 데이터 가져오기 실패 (시도 {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(1)  # 재시도 전 1초 대기
            else:
                return None

    return None


def fetch_kr_etf_data(ticker: str, retries: int = config.MAX_RETRIES) -> Optional[Dict]:
    """
    한국 ETF 데이터를 FinanceDataReader로 가져옵니다.

    Args:
        ticker: ETF 종목코드 (예: "479920", "371460")
        retries: 재시도 횟수

    Returns:
        ETF 데이터 딕셔너리 또는 None (실패 시)
        {
            'ticker': str,
            'name': str,
            'price': float,
            'change': float,
            'change_percent': float,
            'dividend_yield': float,  # 한국 ETF는 배당률 제공 안 됨 (수동 입력 필요)
            'currency': str
        }
    """
    for attempt in range(retries):
        try:
            # 최근 2일 데이터 가져오기 (현재가, 전일가 비교용)
            df = fdr.DataReader(ticker, start='2024-01-01')  # 충분한 기간

            if df.empty:
                print(f"⚠️ {ticker} 데이터가 비어있습니다.")
                return None

            # 최근 2일 데이터 추출
            recent_data = df.tail(2)

            if len(recent_data) < 1:
                print(f"⚠️ {ticker} 최근 데이터가 부족합니다.")
                return None

            # 현재가 (가장 최근 종가)
            current_price = recent_data['Close'].iloc[-1]

            # 전일가
            if len(recent_data) >= 2:
                previous_close = recent_data['Close'].iloc[-2]
            else:
                previous_close = current_price

            # 등락액 및 등락률 계산
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close != 0 else 0

            # 종목명은 별도 API 필요 (간단히 티커로 대체)
            # 실제로는 KRX 종목정보 API를 사용해야 함
            name = ticker  # 추후 개선 가능

            return {
                'ticker': ticker,
                'name': name,
                'price': current_price,
                'change': change,
                'change_percent': change_percent,
                'dividend_yield': 0,  # 한국 ETF 배당률은 수동 관리 필요
                'currency': 'KRW'
            }

        except Exception as e:
            print(f"⚠️ {ticker} 데이터 가져오기 실패 (시도 {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(1)  # 재시도 전 1초 대기
            else:
                return None

    return None


def fetch_exchange_rate() -> float:
    """
    현재 USD/KRW 환율을 가져옵니다.

    Returns:
        환율 (실패 시 기본값 반환)
    """
    try:
        # yfinance로 USD/KRW 환율 조회
        usd_krw = yf.Ticker("KRW=X")
        rate = usd_krw.info.get('regularMarketPrice')

        if rate and rate > 0:
            return rate
        else:
            # 대안: FinanceDataReader 사용
            df = fdr.DataReader('USD/KRW', start='2024-01-01')
            if not df.empty:
                return df['Close'].iloc[-1]
            else:
                return config.DEFAULT_USD_KRW
    except Exception as e:
        print(f"⚠️ 환율 가져오기 실패: {e}. 기본 환율({config.DEFAULT_USD_KRW}) 사용")
        return config.DEFAULT_USD_KRW


def load_watchlist(file_path: str) -> pd.DataFrame:
    """
    CSV 파일에서 관심 종목 목록을 로드합니다.

    Args:
        file_path: CSV 파일 경로

    Returns:
        pandas DataFrame
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ CSV 로드 실패: {e}")
        return pd.DataFrame()


def enrich_watchlist_with_data(watchlist_df: pd.DataFrame, is_us: bool = False) -> pd.DataFrame:
    """
    관심 종목 목록에 실시간 데이터를 추가합니다.

    Args:
        watchlist_df: 관심 종목 DataFrame
        is_us: 미국 주식 여부

    Returns:
        데이터가 추가된 DataFrame
    """
    enriched_data = []

    for _, row in watchlist_df.iterrows():
        ticker = str(row['ticker'])  # 문자열로 변환 (CSV에서 int로 읽힐 수 있음)

        # 데이터 가져오기
        if is_us:
            data = fetch_us_etf_data(ticker)
        else:
            data = fetch_kr_etf_data(ticker)

        if data:
            # 기존 정보 + 새 데이터 병합
            # CSV에 dividend_yield가 있으면 우선 사용 (한국 ETF용)
            csv_dividend = row.get('dividend_yield', None)
            final_dividend = csv_dividend if csv_dividend is not None else data['dividend_yield']

            enriched_row = {
                'ticker': ticker,
                'name': row.get('name', data['name']),
                'type': row.get('type', ''),
                'target_ratio': row.get('target_ratio', 0),
                'price': data['price'],
                'change': data['change'],
                'change_percent': data['change_percent'],
                'dividend_yield': final_dividend,
                'currency': data['currency']
            }
        else:
            # 데이터 가져오기 실패 시 기본값
            enriched_row = {
                'ticker': ticker,
                'name': row.get('name', ticker),
                'type': row.get('type', ''),
                'target_ratio': row.get('target_ratio', 0),
                'price': None,
                'change': None,
                'change_percent': None,
                'dividend_yield': row.get('dividend_yield', None),
                'currency': 'USD' if is_us else 'KRW'
            }

        enriched_data.append(enriched_row)

    return pd.DataFrame(enriched_data)
