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

            # 종목명 가져오기 시도 (ETF 리스트에서 또는 주식 리스트에서)
            name = ticker  # 기본값
            try:
                # ETF 리스트에서 검색
                etf_list = fdr.StockListing('ETF/KR')
                if not etf_list.empty:
                    code_col = 'Code' if 'Code' in etf_list.columns else 'Symbol' if 'Symbol' in etf_list.columns else None
                    name_col = 'Name' if 'Name' in etf_list.columns else None

                    if code_col and name_col:
                        matched = etf_list[etf_list[code_col].astype(str) == str(ticker)]
                        if not matched.empty:
                            name = matched.iloc[0][name_col]

                # ETF에 없으면 주식 리스트에서 검색
                if name == ticker:
                    stock_list = fdr.StockListing('KRX')
                    if not stock_list.empty:
                        code_col = 'Code' if 'Code' in stock_list.columns else 'Symbol' if 'Symbol' in stock_list.columns else None
                        name_col = 'Name' if 'Name' in stock_list.columns else None

                        if code_col and name_col:
                            matched = stock_list[stock_list[code_col].astype(str) == str(ticker)]
                            if not matched.empty:
                                name = matched.iloc[0][name_col]
            except Exception as e:
                print(f"⚠️ {ticker} 종목명 조회 실패: {e}")

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


def fetch_hot_us_stocks(period: str = '1d', limit: int = 10) -> pd.DataFrame:
    """
    미국 S&P 500 상승률 Top 종목을 가져옵니다.

    Args:
        period: 기간 ('1d', '5d', '1mo')
        limit: 상위 몇 개 (기본 10개)

    Returns:
        상승률 상위 종목 DataFrame
    """
    try:
        # S&P 500 구성 종목 가져오기
        sp500 = yf.Ticker("^GSPC")

        # S&P 500 주요 종목 리스트 (상위 100개 정도만 체크 - 속도 최적화)
        # 실제로는 API로 전체 리스트를 가져와야 하지만, 여기서는 주요 종목만
        major_tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'UNH', 'JNJ',
            'V', 'XOM', 'WMT', 'JPM', 'MA', 'PG', 'AVGO', 'HD', 'CVX', 'MRK',
            'LLY', 'ABBV', 'PEP', 'KO', 'COST', 'MCD', 'TMO', 'CSCO', 'ACN', 'ADBE',
            'NKE', 'ABT', 'DHR', 'TXN', 'CRM', 'NEE', 'VZ', 'INTC', 'WFC', 'CMCSA',
            'AMD', 'QCOM', 'PM', 'UNP', 'ORCL', 'BMY', 'HON', 'AMGN', 'RTX', 'UPS'
        ]

        hot_stocks = []

        for ticker in major_tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period='5d' if period == '1d' else '1mo')

                if len(hist) < 2:
                    continue

                # 기간별 수익률 계산
                if period == '1d':
                    start_price = hist['Close'].iloc[-2]
                    end_price = hist['Close'].iloc[-1]
                elif period == '5d':
                    start_price = hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                else:  # 1mo
                    start_price = hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]

                change_percent = ((end_price - start_price) / start_price) * 100

                # 기본 정보 가져오기
                info = stock.info
                name = info.get('shortName', ticker)
                current_price = hist['Close'].iloc[-1]
                volume = hist['Volume'].iloc[-1]
                dividend_yield = info.get('dividendYield', 0)

                hot_stocks.append({
                    'ticker': ticker,
                    'name': name,
                    'price': current_price,
                    'change_percent': change_percent,
                    'volume': volume,
                    'dividend_yield': dividend_yield,
                    'currency': 'USD'
                })

            except Exception as e:
                print(f"⚠️ {ticker} 데이터 가져오기 실패: {e}")
                continue

        # DataFrame 생성 및 정렬
        df = pd.DataFrame(hot_stocks)
        if not df.empty:
            df = df.sort_values('change_percent', ascending=False).head(limit)
            df = df.reset_index(drop=True)

        return df

    except Exception as e:
        print(f"❌ HOT 미국 주식 데이터 가져오기 실패: {e}")
        return pd.DataFrame()


def fetch_hot_kr_etfs(period: str = '1d', limit: int = 10) -> pd.DataFrame:
    """
    한국 ETF 수익률 Top 종목을 가져옵니다.

    Args:
        period: 기간 ('1d', '5d', '1mo')
        limit: 상위 몇 개 (기본 10개)

    Returns:
        수익률 상위 ETF DataFrame
    """
    try:
        # 한국 전체 ETF 리스트 가져오기
        etf_list = fdr.StockListing('ETF/KR')

        if etf_list.empty:
            print("⚠️ 한국 ETF 리스트를 가져올 수 없습니다.")
            return pd.DataFrame()

        # 컬럼명 확인 (디버깅용)
        print(f"📋 ETF 리스트 컬럼: {etf_list.columns.tolist()}")

        hot_etfs = []

        # 상위 50개 ETF만 체크 (속도 최적화 - 200개에서 50개로 감소)
        for idx, etf_row in etf_list.head(50).iterrows():
            # 컬럼명이 'Code' 또는 'Symbol' 또는 인덱스일 수 있음
            if 'Code' in etf_list.columns:
                ticker = str(etf_row['Code'])
            elif 'Symbol' in etf_list.columns:
                ticker = str(etf_row['Symbol'])
            else:
                ticker = str(etf_row.name)  # 인덱스가 티커인 경우

            if 'Name' in etf_list.columns:
                name = etf_row['Name']
            else:
                name = ticker

            try:
                # 기간별 데이터 가져오기
                if period == '1d':
                    df = fdr.DataReader(ticker, start='2024-01-01')
                    if len(df) < 2:
                        continue
                    start_price = df['Close'].iloc[-2]
                    end_price = df['Close'].iloc[-1]
                elif period == '5d':
                    df = fdr.DataReader(ticker, start='2024-01-01')
                    if len(df) < 5:
                        continue
                    start_price = df['Close'].iloc[-6]
                    end_price = df['Close'].iloc[-1]
                else:  # 1mo
                    df = fdr.DataReader(ticker, start='2023-12-01')
                    if len(df) < 20:
                        continue
                    start_price = df['Close'].iloc[-21]
                    end_price = df['Close'].iloc[-1]

                change_percent = ((end_price - start_price) / start_price) * 100
                volume = df['Volume'].iloc[-1]

                hot_etfs.append({
                    'ticker': ticker,
                    'name': name,
                    'price': end_price,
                    'change_percent': change_percent,
                    'volume': volume,
                    'dividend_yield': 0,  # 한국 ETF는 배당률 데이터 없음
                    'currency': 'KRW'
                })

            except Exception as e:
                # 개별 종목 실패는 조용히 넘어감 (로그만 출력)
                continue

        # DataFrame 생성 및 정렬
        df = pd.DataFrame(hot_etfs)
        if not df.empty:
            df = df.sort_values('change_percent', ascending=False).head(limit)
            df = df.reset_index(drop=True)

        return df

    except Exception as e:
        print(f"❌ HOT 한국 ETF 데이터 가져오기 실패: {e}")
        return pd.DataFrame()


def search_stock_multiple(query: str) -> list:
    """
    종목 티커 또는 종목명으로 검색하여 매칭되는 모든 종목 리스트를 반환합니다.

    Args:
        query: 검색할 티커 또는 종목명 (예: "AAPL", "005930", "삼성전자", "커버드콜")

    Returns:
        매칭된 종목들의 리스트 (각 항목은 {'ticker', 'name', 'market'} 딕셔너리)
    """
    query = query.strip()
    results = []

    if not query:
        return results

    # 1. 한글이 포함되어 있으면 바로 한국 ETF 리스트 검색
    if any('\uac00' <= char <= '\ud7a3' for char in query):
        try:
            # 한국 ETF 리스트 가져오기
            etf_list = fdr.StockListing('ETF/KR')

            if not etf_list.empty:
                # 종목명 컬럼 확인
                name_col = 'Name' if 'Name' in etf_list.columns else None
                code_col = 'Code' if 'Code' in etf_list.columns else 'Symbol' if 'Symbol' in etf_list.columns else None

                if name_col and code_col:
                    # 종목명에 검색어가 포함되는 ETF 찾기 (최대 10개)
                    matched = etf_list[etf_list[name_col].str.contains(query, case=False, na=False)].head(10)

                    for _, row in matched.iterrows():
                        results.append({
                            'ticker': str(row[code_col]),
                            'name': row[name_col],
                            'market': 'KR'
                        })
                    return results  # 한글 검색은 여기서 종료
        except Exception as e:
            print(f"⚠️ 한국어 종목명 검색 실패: {e}")
        return results

    # 2. 숫자로만 이루어진 티커는 한국 주식/ETF (005930 같은 형태)
    if query.isdigit():
        try:
            # 먼저 리스트에서 종목명 찾기
            ticker_name = query
            try:
                # ETF 리스트에서 검색
                etf_list = fdr.StockListing('ETF/KR')
                if not etf_list.empty:
                    code_col = 'Code' if 'Code' in etf_list.columns else 'Symbol' if 'Symbol' in etf_list.columns else None
                    name_col = 'Name' if 'Name' in etf_list.columns else None

                    if code_col and name_col:
                        matched = etf_list[etf_list[code_col].astype(str) == str(query)]
                        if not matched.empty:
                            ticker_name = matched.iloc[0][name_col]

                # ETF에 없으면 주식 리스트에서 검색
                if ticker_name == query:
                    stock_list = fdr.StockListing('KRX')
                    if not stock_list.empty:
                        code_col = 'Code' if 'Code' in stock_list.columns else 'Symbol' if 'Symbol' in stock_list.columns else None
                        name_col = 'Name' if 'Name' in stock_list.columns else None

                        if code_col and name_col:
                            matched = stock_list[stock_list[code_col].astype(str) == str(query)]
                            if not matched.empty:
                                ticker_name = matched.iloc[0][name_col]
            except:
                pass

            # 데이터가 있는지 확인
            kr_data = fetch_kr_etf_data(query)
            if kr_data:
                results.append({
                    'ticker': query,
                    'name': ticker_name,  # 리스트에서 찾은 종목명 사용
                    'market': 'KR'
                })
                return results  # 티커 정확히 일치하면 바로 반환
        except:
            pass

    # 3. 알파벳이 포함된 경우 미국 주식으로 시도
    try:
        us_data = fetch_us_etf_data(query.upper())
        if us_data:
            results.append({
                'ticker': query.upper(),
                'name': us_data.get('name', query.upper()),
                'market': 'US'
            })
            return results
    except:
        pass

    return results


def search_stock(query: str) -> Optional[Dict]:
    """
    종목 티커 또는 종목명으로 검색하여 정보를 가져옵니다.

    Args:
        query: 검색할 티커 또는 종목명 (예: "AAPL", "005930", "삼성전자", "커버드콜")

    Returns:
        종목 정보 딕셔너리 또는 None
    """
    query = query.strip()

    if not query:
        return None

    # 1. 먼저 미국 주식으로 티커 검색 시도 (대문자 변환)
    try:
        us_data = fetch_us_etf_data(query.upper())
        if us_data:
            us_data['market'] = 'US'
            return us_data
    except:
        pass

    # 2. 한국 주식/ETF 티커로 검색 시도
    try:
        kr_data = fetch_kr_etf_data(query)
        if kr_data:
            kr_data['market'] = 'KR'
            return kr_data
    except:
        pass

    # 3. 한국어 종목명으로 검색 (한글이 포함된 경우)
    if any('\uac00' <= char <= '\ud7a3' for char in query):
        try:
            # 한국 ETF 리스트 가져오기
            etf_list = fdr.StockListing('ETF/KR')

            if not etf_list.empty:
                # 종목명 컬럼 확인
                name_col = 'Name' if 'Name' in etf_list.columns else None
                code_col = 'Code' if 'Code' in etf_list.columns else 'Symbol' if 'Symbol' in etf_list.columns else None

                if name_col and code_col:
                    # 종목명에 검색어가 포함되는 ETF 찾기
                    matched = etf_list[etf_list[name_col].str.contains(query, case=False, na=False)]

                    if not matched.empty:
                        # 첫 번째 매칭 결과 사용
                        first_match = matched.iloc[0]
                        ticker = str(first_match[code_col])

                        # 해당 티커로 데이터 가져오기
                        kr_data = fetch_kr_etf_data(ticker)
                        if kr_data:
                            kr_data['market'] = 'KR'
                            kr_data['name'] = first_match[name_col]  # 정확한 종목명 사용
                            return kr_data
        except Exception as e:
            print(f"⚠️ 한국어 종목명 검색 실패: {e}")

    return None
