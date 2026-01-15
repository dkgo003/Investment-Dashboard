"""
투자 대시보드 메인 애플리케이션
Streamlit 기반 개인 투자 포트폴리오 대시보드
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import config
import data_fetcher
import utils


# 페이지 설정
st.set_page_config(
    page_title="투자 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 제목
st.title("📊 투자 포트폴리오 대시보드")
st.markdown("---")


# 세션 상태 초기화 (임시 워치리스트)
if 'temp_watchlist_isa' not in st.session_state:
    st.session_state.temp_watchlist_isa = []
if 'temp_watchlist_direct' not in st.session_state:
    st.session_state.temp_watchlist_direct = []


# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")

    # 새로고침 버튼
    if st.button("🔄 데이터 새로고침", width='stretch'):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")

    # 환율 정보
    st.subheader("💱 환율 정보")
    exchange_rate = data_fetcher.fetch_exchange_rate()
    st.metric("USD/KRW", f"₩{exchange_rate:,.2f}")

    st.markdown("---")

    # 종목 검색
    st.subheader("🔍 종목 검색")
    search_query = st.text_input(
        "티커 또는 종목명 입력",
        key="search_input",
        placeholder="AAPL, 삼성전자, 커버드콜..."
    )

    if search_query:
        with st.spinner("검색 중..."):
            search_results = data_fetcher.search_stock_multiple(search_query)

        if search_results:
            # 여러 결과가 있으면 선택 UI 표시
            if len(search_results) > 1:
                st.info(f"🔍 {len(search_results)}개의 종목이 발견되었습니다. 클릭하여 상세 정보를 확인하세요.")

                # 세션 스테이트에 선택된 종목 저장
                if 'selected_stock' not in st.session_state:
                    st.session_state.selected_stock = None

                for idx, result in enumerate(search_results):
                    with st.expander(f"📊 {result['name']} ({result['ticker']})"):
                        # 선택 버튼
                        if st.button(f"이 종목 선택", key=f"select_{result['ticker']}_{idx}"):
                            st.session_state.selected_stock = result['ticker']
                            st.rerun()

                        # 선택된 종목이면 상세 정보 표시
                        if st.session_state.selected_stock == result['ticker']:
                            with st.spinner("상세 정보 로딩 중..."):
                                if result['market'] == 'US':
                                    stock_detail = data_fetcher.fetch_us_etf_data(result['ticker'])
                                else:
                                    stock_detail = data_fetcher.fetch_kr_etf_data(result['ticker'])

                            if stock_detail and stock_detail.get('price') is not None:
                                stock_detail['market'] = result['market']

                                col1, col2 = st.columns(2)
                                with col1:
                                    if stock_detail['market'] == 'US':
                                        st.metric("현재가", f"${stock_detail['price']:.2f}")
                                    else:
                                        st.metric("현재가", f"₩{stock_detail['price']:,.0f}")

                                with col2:
                                    change_pct = stock_detail.get('change_percent', 0)
                                    st.metric("등락률", f"{change_pct:+.2f}%")

                                # 배당률
                                div_yield = stock_detail.get('dividend_yield')
                                if div_yield is not None and div_yield > 0:
                                    st.caption(f"배당률: {div_yield:.2f}%")

                                # 임시 워치리스트 추가 버튼
                                st.markdown("---")

                                if stock_detail['market'] == 'US':
                                    if st.button("➕ 미국 직투 임시 워치리스트에 추가", key=f"add_us_{result['ticker']}_{idx}", width='stretch'):
                                        if stock_detail['ticker'] not in [item['ticker'] for item in st.session_state.temp_watchlist_direct]:
                                            st.session_state.temp_watchlist_direct.append({
                                                'ticker': stock_detail['ticker'],
                                                'name': stock_detail['name'],
                                                'type': '검색 종목',
                                                'price': stock_detail['price'],
                                                'change_percent': stock_detail.get('change_percent', 0),
                                                'dividend_yield': stock_detail.get('dividend_yield', 0),
                                                'currency': 'USD'
                                            })
                                            st.success("추가 완료!")
                                            st.rerun()
                                        else:
                                            st.warning("이미 추가된 종목입니다.")
                                else:  # KR
                                    if st.button("➕ ISA 임시 워치리스트에 추가", key=f"add_kr_{result['ticker']}_{idx}", width='stretch'):
                                        if stock_detail['ticker'] not in [item['ticker'] for item in st.session_state.temp_watchlist_isa]:
                                            st.session_state.temp_watchlist_isa.append({
                                                'ticker': stock_detail['ticker'],
                                                'name': stock_detail['name'],
                                                'type': '검색 종목',
                                                'price': stock_detail['price'],
                                                'change_percent': stock_detail.get('change_percent', 0),
                                                'dividend_yield': stock_detail.get('dividend_yield', 0),
                                                'currency': 'KRW'
                                            })
                                            st.success("추가 완료!")
                                            st.rerun()
                                        else:
                                            st.warning("이미 추가된 종목입니다.")
                            else:
                                st.error(f"❌ '{result['name']}' 종목의 상세 정보를 가져올 수 없습니다.")

            # 결과가 1개면 바로 표시
            else:
                result = search_results[0]
                with st.spinner("상세 정보 로딩 중..."):
                    if result['market'] == 'US':
                        search_result = data_fetcher.fetch_us_etf_data(result['ticker'])
                    else:
                        search_result = data_fetcher.fetch_kr_etf_data(result['ticker'])

                if search_result and search_result.get('price') is not None:
                    search_result['market'] = result['market']
                    st.success(f"✅ {search_result['name']} 발견!")

                    # 검색 결과 표시
                    with st.container():
                        st.markdown(f"**{search_result['ticker']}** - {search_result['name']}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if search_result['market'] == 'US':
                                st.metric("현재가", f"${search_result['price']:.2f}")
                            else:
                                st.metric("현재가", f"₩{search_result['price']:,.0f}")

                        with col2:
                            change_pct = search_result.get('change_percent', 0)
                            st.metric("등락률", f"{change_pct:+.2f}%")

                        # 배당률
                        div_yield = search_result.get('dividend_yield')
                        if div_yield is not None and div_yield > 0:
                            st.caption(f"배당률: {div_yield:.2f}%")

                        # 임시 워치리스트 추가 버튼
                        st.markdown("---")

                        if search_result['market'] == 'US':
                            if st.button("➕ 미국 직투 임시 워치리스트에 추가", key="add_search_us", width='stretch'):
                                if search_result['ticker'] not in [item['ticker'] for item in st.session_state.temp_watchlist_direct]:
                                    st.session_state.temp_watchlist_direct.append({
                                        'ticker': search_result['ticker'],
                                        'name': search_result['name'],
                                        'type': '검색 종목',
                                        'price': search_result['price'],
                                        'change_percent': search_result.get('change_percent', 0),
                                        'dividend_yield': search_result.get('dividend_yield', 0),
                                        'currency': 'USD'
                                    })
                                    st.success("추가 완료!")
                                    st.rerun()
                                else:
                                    st.warning("이미 추가된 종목입니다.")
                        else:  # KR
                            if st.button("➕ ISA 임시 워치리스트에 추가", key="add_search_kr", width='stretch'):
                                if search_result['ticker'] not in [item['ticker'] for item in st.session_state.temp_watchlist_isa]:
                                    st.session_state.temp_watchlist_isa.append({
                                        'ticker': search_result['ticker'],
                                        'name': search_result['name'],
                                        'type': '검색 종목',
                                        'price': search_result['price'],
                                        'change_percent': search_result.get('change_percent', 0),
                                        'dividend_yield': search_result.get('dividend_yield', 0),
                                        'currency': 'KRW'
                                    })
                                    st.success("추가 완료!")
                                    st.rerun()
                                else:
                                    st.warning("이미 추가된 종목입니다.")
                else:
                    st.error(f"❌ '{result['name']}' 종목의 상세 정보를 가져올 수 없습니다.")
        else:
            st.error(f"❌ '{search_query}' 종목을 찾을 수 없습니다.")

    st.markdown("---")

    # 마지막 업데이트 시간
    st.caption(f"⏰ 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# 캐시를 사용한 데이터 로드 함수
@st.cache_data(ttl=config.CACHE_TTL)
def load_isa_data():
    """ISA 관심 종목 데이터 로드 (캐시 사용)"""
    watchlist = data_fetcher.load_watchlist(str(config.ISA_WATCHLIST_PATH))
    if watchlist.empty:
        return pd.DataFrame()
    return data_fetcher.enrich_watchlist_with_data(watchlist, is_us=False)


@st.cache_data(ttl=config.CACHE_TTL)
def load_direct_data():
    """미국 직투 관심 종목 데이터 로드 (캐시 사용)"""
    watchlist = data_fetcher.load_watchlist(str(config.DIRECT_WATCHLIST_PATH))
    if watchlist.empty:
        return pd.DataFrame()
    return data_fetcher.enrich_watchlist_with_data(watchlist, is_us=True)


# HOT 종목 데이터 로드 함수
@st.cache_data(ttl=config.CACHE_TTL)
def load_hot_us_data(period='1d'):
    """HOT 미국 주식 데이터 로드 (캐시 사용)"""
    return data_fetcher.fetch_hot_us_stocks(period=period, limit=10)


@st.cache_data(ttl=config.CACHE_TTL)
def load_hot_kr_data(period='1d'):
    """HOT 한국 ETF 데이터 로드 (캐시 사용)"""
    return data_fetcher.fetch_hot_kr_etfs(period=period, limit=10)


# 탭 생성
tab_isa, tab_direct, tab_hot, tab_summary = st.tabs(["🇰🇷 ISA 계좌", "🇺🇸 미국 직투", "🔥 HOT 종목 Top 10", "📈 전체 요약"])


# ==================== ISA 계좌 탭 ====================
with tab_isa:
    st.header("🇰🇷 ISA 계좌 - 국내 상장 ETF")

    # 데이터 로드
    with st.spinner("데이터를 불러오는 중..."):
        isa_data = load_isa_data()

    if isa_data.empty:
        st.error("❌ ISA 관심 종목 데이터를 불러올 수 없습니다.")
    else:
        # ETF 카드 표시
        num_cols = 3
        cols = st.columns(num_cols)

        for idx, row in isa_data.iterrows():
            col_idx = idx % num_cols

            with cols[col_idx]:
                # 카드 컨테이너
                with st.container():
                    # 종목명 및 티커
                    st.subheader(f"{row['name']}")
                    st.caption(f"종목코드: {row['ticker']} | {row['type']}")

                    # 가격 정보
                    if row['price'] is not None:
                        # 등락률 색상
                        change_color = utils.get_color_for_change(row['change_percent'])

                        # 현재가
                        st.metric(
                            label="현재가",
                            value=utils.format_price(row['price'], "KRW"),
                            delta=utils.format_percent(row['change_percent'])
                        )

                        # 추가 정보
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("등락액", utils.format_price(row['change'], "KRW"))
                        with col2:
                            st.metric("배당률", utils.format_ratio(row['dividend_yield']) if row['dividend_yield'] else "N/A")
                        with col3:
                            st.metric("목표 비중", utils.format_ratio(row['target_ratio']))
                    else:
                        st.warning("⚠️ 데이터를 불러올 수 없습니다.")

                    st.markdown("---")

        # 포트폴리오 요약 테이블
        st.subheader("📊 ISA 포트폴리오 요약")

        summary_df = isa_data[['ticker', 'name', 'price', 'change_percent', 'dividend_yield', 'target_ratio']].copy()
        summary_df.columns = ['종목코드', '종목명', '현재가 (원)', '등락률 (%)', '배당률 (%)', '목표 비중 (%)']

        # 포맷팅 함수 (None 처리 포함)
        def format_price_safe(val):
            if val is None or pd.isna(val):
                return "N/A"
            return f"{val:,.0f}"

        def format_percent_safe(val):
            if val is None or pd.isna(val):
                return "N/A"
            return f"{val:+.2f}"

        def format_dividend_safe(val):
            if val is None or pd.isna(val):
                return "N/A"
            return f"{val:.1f}"

        def format_ratio_safe(val):
            if val is None or pd.isna(val):
                return "N/A"
            return f"{val:.1f}"

        # 포맷팅 적용
        st.dataframe(
            summary_df.style.format({
                '현재가 (원)': format_price_safe,
                '등락률 (%)': format_percent_safe,
                '배당률 (%)': format_dividend_safe,
                '목표 비중 (%)': format_ratio_safe
            }),
            width='stretch',
            hide_index=True
        )

    # 임시 관심 종목 섹션
    st.markdown("---")
    st.subheader("⭐ 임시 관심 종목")

    if len(st.session_state.temp_watchlist_isa) == 0:
        st.info("💡 HOT 종목 탭에서 종목을 추가해보세요!")
    else:
        st.caption(f"총 {len(st.session_state.temp_watchlist_isa)}개 종목")

        for idx, item in enumerate(st.session_state.temp_watchlist_isa):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

                with col1:
                    st.markdown(f"**{item['name']}** ({item['ticker']})")

                with col2:
                    st.metric("현재가", f"₩{item['price']:,.0f}")

                with col3:
                    change_color = "🔴" if item['change_percent'] < 0 else "🟢"
                    st.markdown(f"{change_color} {item['change_percent']:+.2f}%")

                with col4:
                    # 삭제 버튼
                    if st.button("🗑️", key=f"remove_isa_{idx}", help="임시 워치리스트에서 제거"):
                        st.session_state.temp_watchlist_isa.pop(idx)
                        st.rerun()

                # 영구 저장 기능 (CSV 추가)
                with st.expander("💾 영구 저장 (CSV에 추가)"):
                    target_ratio = st.number_input(
                        "목표 비중 (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=10.0,
                        step=5.0,
                        key=f"ratio_isa_{idx}"
                    )

                    if st.button("CSV에 저장", key=f"save_isa_{idx}"):
                        # CSV에 추가
                        import csv
                        with open(config.ISA_WATCHLIST_PATH, 'a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow([
                                item['ticker'],
                                item['name'],
                                item['type'],
                                target_ratio,
                                0  # dividend_yield (수동 입력 필요)
                            ])
                        st.success(f"✅ {item['name']}이(가) CSV에 저장되었습니다!")
                        st.info("📝 캐시를 새로고침하려면 사이드바의 '데이터 새로고침' 버튼을 클릭하세요.")

                st.markdown("---")


# ==================== 미국 직투 탭 ====================
with tab_direct:
    st.header("🇺🇸 미국 직투 계좌 - 미국 상장 ETF")

    # 데이터 로드
    with st.spinner("데이터를 불러오는 중..."):
        direct_data = load_direct_data()

    if direct_data.empty:
        st.error("❌ 미국 직투 관심 종목 데이터를 불러올 수 없습니다.")
    else:
        # ETF 카드 표시
        num_cols = 2
        cols = st.columns(num_cols)

        for idx, row in direct_data.iterrows():
            col_idx = idx % num_cols

            with cols[col_idx]:
                # 카드 컨테이너
                with st.container():
                    # 종목명 및 티커
                    st.subheader(f"{row['ticker']}")
                    st.caption(f"{row['name']} | {row['type']}")

                    # 가격 정보
                    if row['price'] is not None:
                        # 현재가
                        st.metric(
                            label="현재가 (USD)",
                            value=utils.format_price(row['price'], "USD"),
                            delta=utils.format_percent(row['change_percent'])
                        )

                        # 원화 환산 가격
                        krw_price = utils.convert_usd_to_krw(row['price'], exchange_rate)
                        st.caption(f"원화 환산: {utils.format_price(krw_price, 'KRW')}")

                        # 추가 정보
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("등락액", utils.format_price(row['change'], "USD"))
                        with col2:
                            st.metric("배당률", utils.format_ratio(row['dividend_yield']))
                        with col3:
                            st.metric("목표 비중", utils.format_ratio(row['target_ratio']))
                    else:
                        st.warning("⚠️ 데이터를 불러올 수 없습니다.")

                    st.markdown("---")

        # 포트폴리오 요약 테이블
        st.subheader("📊 미국 직투 포트폴리오 요약")

        summary_df = direct_data[['ticker', 'name', 'price', 'change_percent', 'dividend_yield', 'target_ratio']].copy()
        summary_df.columns = ['티커', '종목명', '현재가 (USD)', '등락률 (%)', '배당률 (%)', '목표 비중 (%)']

        # 포맷팅 함수 (None 처리 포함)
        def format_usd_safe(val):
            if val is None or pd.isna(val):
                return "N/A"
            return f"${val:.2f}"

        def format_percent_safe(val):
            if val is None or pd.isna(val):
                return "N/A"
            return f"{val:+.2f}"

        def format_dividend_safe(val):
            if val is None or pd.isna(val):
                return "N/A"
            return f"{val:.2f}"

        def format_ratio_safe(val):
            if val is None or pd.isna(val):
                return "N/A"
            return f"{val:.1f}"

        # 포맷팅 적용
        st.dataframe(
            summary_df.style.format({
                '현재가 (USD)': format_usd_safe,
                '등락률 (%)': format_percent_safe,
                '배당률 (%)': format_dividend_safe,
                '목표 비중 (%)': format_ratio_safe
            }),
            width='stretch',
            hide_index=True
        )

    # 임시 관심 종목 섹션
    st.markdown("---")
    st.subheader("⭐ 임시 관심 종목")

    if len(st.session_state.temp_watchlist_direct) == 0:
        st.info("💡 HOT 종목 탭에서 종목을 추가해보세요!")
    else:
        st.caption(f"총 {len(st.session_state.temp_watchlist_direct)}개 종목")

        for idx, item in enumerate(st.session_state.temp_watchlist_direct):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

                with col1:
                    st.markdown(f"**{item['ticker']}** - {item['name']}")

                with col2:
                    st.metric("현재가", f"${item['price']:.2f}")

                with col3:
                    change_color = "🔴" if item['change_percent'] < 0 else "🟢"
                    st.markdown(f"{change_color} {item['change_percent']:+.2f}%")

                with col4:
                    # 삭제 버튼
                    if st.button("🗑️", key=f"remove_direct_{idx}", help="임시 워치리스트에서 제거"):
                        st.session_state.temp_watchlist_direct.pop(idx)
                        st.rerun()

                # 영구 저장 기능 (CSV 추가)
                with st.expander("💾 영구 저장 (CSV에 추가)"):
                    target_ratio = st.number_input(
                        "목표 비중 (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=10.0,
                        step=5.0,
                        key=f"ratio_direct_{idx}"
                    )

                    if st.button("CSV에 저장", key=f"save_direct_{idx}"):
                        # CSV에 추가
                        import csv
                        with open(config.DIRECT_WATCHLIST_PATH, 'a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow([
                                item['ticker'],
                                item['name'],
                                item['type'],
                                target_ratio
                            ])
                        st.success(f"✅ {item['ticker']}이(가) CSV에 저장되었습니다!")
                        st.info("📝 캐시를 새로고침하려면 사이드바의 '데이터 새로고침' 버튼을 클릭하세요.")

                st.markdown("---")


# ==================== HOT 종목 Top 10 탭 ====================
with tab_hot:
    st.header("🔥 HOT 종목 Top 10")
    st.caption("상승률 기준 인기 종목 (클릭하여 임시 워치리스트에 추가)")

    # 기간 선택
    period_option = st.radio(
        "기간 선택",
        ["일일", "주간", "월간"],
        horizontal=True,
        key="hot_period"
    )

    period_map = {"일일": "1d", "주간": "5d", "월간": "1mo"}
    selected_period = period_map[period_option]

    st.markdown("---")

    # 미국 주식 & 한국 ETF 섹션
    col_us, col_kr = st.columns(2)

    # 미국 HOT 주식
    with col_us:
        st.subheader("🇺🇸 미국 HOT 주식 (S&P 500 주요 종목)")

        with st.spinner("미국 HOT 주식 데이터 로딩 중..."):
            hot_us_data = load_hot_us_data(period=selected_period)

        if hot_us_data.empty:
            st.warning("⚠️ 데이터를 불러올 수 없습니다.")
        else:
            for idx, row in hot_us_data.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        st.markdown(f"**{idx + 1}. {row['ticker']}** - {row['name']}")

                    with col2:
                        change_color = "🔴" if row['change_percent'] < 0 else "🟢"
                        st.markdown(f"{change_color} **{row['change_percent']:+.2f}%**")

                    with col3:
                        # 임시 워치리스트에 추가 버튼
                        if st.button("➕", key=f"add_us_{row['ticker']}", help="미국 직투 임시 워치리스트에 추가"):
                            # 중복 체크
                            if row['ticker'] not in [item['ticker'] for item in st.session_state.temp_watchlist_direct]:
                                st.session_state.temp_watchlist_direct.append({
                                    'ticker': row['ticker'],
                                    'name': row['name'],
                                    'type': '임시 종목',
                                    'price': row['price'],
                                    'change_percent': row['change_percent'],
                                    'dividend_yield': row['dividend_yield'],
                                    'currency': 'USD'
                                })
                                st.success(f"✅ {row['ticker']} 추가됨!")
                                st.rerun()
                            else:
                                st.warning("이미 추가된 종목입니다.")

                    st.caption(f"가격: ${row['price']:.2f} | 배당률: {row['dividend_yield']:.2f}%")
                    st.markdown("---")

    # 한국 HOT ETF
    with col_kr:
        st.subheader("🇰🇷 한국 HOT ETF")

        with st.spinner("한국 HOT ETF 데이터 로딩 중..."):
            hot_kr_data = load_hot_kr_data(period=selected_period)

        if hot_kr_data.empty:
            st.warning("⚠️ 데이터를 불러올 수 없습니다.")
        else:
            for idx, row in hot_kr_data.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        st.markdown(f"**{idx + 1}. {row['ticker']}** - {row['name']}")

                    with col2:
                        change_color = "🔴" if row['change_percent'] < 0 else "🟢"
                        st.markdown(f"{change_color} **{row['change_percent']:+.2f}%**")

                    with col3:
                        # 임시 워치리스트에 추가 버튼
                        if st.button("➕", key=f"add_kr_{row['ticker']}", help="ISA 임시 워치리스트에 추가"):
                            # 중복 체크
                            if row['ticker'] not in [item['ticker'] for item in st.session_state.temp_watchlist_isa]:
                                st.session_state.temp_watchlist_isa.append({
                                    'ticker': row['ticker'],
                                    'name': row['name'],
                                    'type': '임시 종목',
                                    'price': row['price'],
                                    'change_percent': row['change_percent'],
                                    'dividend_yield': 0,
                                    'currency': 'KRW'
                                })
                                st.success(f"✅ {row['name']} 추가됨!")
                                st.rerun()
                            else:
                                st.warning("이미 추가된 종목입니다.")

                    st.caption(f"가격: ₩{row['price']:,.0f}")
                    st.markdown("---")


# ==================== 전체 요약 탭 ====================
with tab_summary:
    st.header("📈 전체 포트폴리오 요약")

    # 데이터 로드
    with st.spinner("데이터를 불러오는 중..."):
        isa_data = load_isa_data()
        direct_data = load_direct_data()

    # 통합 요약
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ISA 관심 종목", f"{len(isa_data)}개")
    with col2:
        st.metric("미국 직투 관심 종목", f"{len(direct_data)}개")
    with col3:
        st.metric("전체 관심 종목", f"{len(isa_data) + len(direct_data)}개")

    st.markdown("---")

    # ISA 계좌 요약
    st.subheader("🇰🇷 ISA 계좌")
    if not isa_data.empty:
        # 간단한 표시 (포맷 없이)
        display_isa = isa_data[['ticker', 'name', 'price', 'change_percent', 'target_ratio']].copy()
        st.dataframe(display_isa, width='stretch', hide_index=True)

    st.markdown("---")

    # 미국 직투 계좌 요약
    st.subheader("🇺🇸 미국 직투 계좌")
    if not direct_data.empty:
        # 간단한 표시 (포맷 없이)
        display_direct = direct_data[['ticker', 'name', 'price', 'change_percent', 'dividend_yield', 'target_ratio']].copy()
        st.dataframe(display_direct, width='stretch', hide_index=True)

    st.markdown("---")

    # 향후 기능 안내
    st.info("""
    💡 **향후 추가 예정 기능**
    - 실제 보유 수량 입력 및 포트폴리오 평가액
    - 총 수익률 계산
    - 월 예상 배당금 계산
    - 리밸런싱 추천
    - 배당 캘린더
    - 금융 뉴스 큐레이션
    - 차트 및 그래프
    """)


# 푸터
st.markdown("---")
st.caption("📊 투자 대시보드 v0.1 | 개인 투자 참고용 | 투자 결정은 본인 책임입니다.")
