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


# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")

    # 새로고침 버튼
    if st.button("🔄 데이터 새로고침", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")

    # 환율 정보
    st.subheader("💱 환율 정보")
    exchange_rate = data_fetcher.fetch_exchange_rate()
    st.metric("USD/KRW", f"₩{exchange_rate:,.2f}")

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


# 탭 생성
tab_isa, tab_direct, tab_summary = st.tabs(["🇰🇷 ISA 계좌", "🇺🇸 미국 직투", "📈 전체 요약"])


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
            use_container_width=True,
            hide_index=True
        )


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
            use_container_width=True,
            hide_index=True
        )


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
        st.dataframe(display_isa, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 미국 직투 계좌 요약
    st.subheader("🇺🇸 미국 직투 계좌")
    if not direct_data.empty:
        # 간단한 표시 (포맷 없이)
        display_direct = direct_data[['ticker', 'name', 'price', 'change_percent', 'dividend_yield', 'target_ratio']].copy()
        st.dataframe(display_direct, use_container_width=True, hide_index=True)

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
