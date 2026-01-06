"""
유틸리티 함수 모듈
데이터 포맷팅, 계산 등의 헬퍼 함수를 제공합니다.
"""

from typing import Union
import config


def format_price(price: Union[float, int], currency: str = "KRW") -> str:
    """
    가격을 포맷팅합니다.

    Args:
        price: 가격 (숫자)
        currency: 통화 ("KRW" 또는 "USD")

    Returns:
        포맷팅된 가격 문자열

    Examples:
        >>> format_price(12345.67, "KRW")
        '₩12,345.67'
        >>> format_price(123.45, "USD")
        '$123.45'
    """
    if price is None:
        return "N/A"

    try:
        formatted = f"{price:,.{config.DECIMAL_PLACES_PRICE}f}"

        if currency == "KRW":
            return f"₩{formatted}"
        elif currency == "USD":
            return f"${formatted}"
        else:
            return formatted
    except (ValueError, TypeError):
        return "N/A"


def format_percent(value: Union[float, int], show_sign: bool = True) -> str:
    """
    퍼센트를 포맷팅합니다.

    Args:
        value: 퍼센트 값 (예: 5.67은 5.67%)
        show_sign: 부호 표시 여부 (True면 +/- 표시)

    Returns:
        포맷팅된 퍼센트 문자열

    Examples:
        >>> format_percent(5.67)
        '+5.67%'
        >>> format_percent(-2.34)
        '-2.34%'
        >>> format_percent(5.67, show_sign=False)
        '5.67%'
    """
    if value is None:
        return "N/A"

    try:
        formatted = f"{value:.{config.DECIMAL_PLACES_PERCENT}f}"

        if show_sign:
            if value > 0:
                return f"+{formatted}%"
            else:
                return f"{formatted}%"
        else:
            return f"{formatted}%"
    except (ValueError, TypeError):
        return "N/A"


def format_ratio(value: Union[float, int]) -> str:
    """
    비율을 포맷팅합니다.

    Args:
        value: 비율 값 (예: 25.5는 25.5%)

    Returns:
        포맷팅된 비율 문자열

    Examples:
        >>> format_ratio(25.5)
        '25.5%'
    """
    if value is None:
        return "N/A"

    try:
        return f"{value:.{config.DECIMAL_PLACES_RATIO}f}%"
    except (ValueError, TypeError):
        return "N/A"


def calculate_target_amount(total_amount: float, target_ratio: float) -> float:
    """
    목표 비중에 따른 목표 금액을 계산합니다.

    Args:
        total_amount: 총 투자 금액
        target_ratio: 목표 비중 (퍼센트, 예: 25는 25%)

    Returns:
        목표 금액

    Examples:
        >>> calculate_target_amount(20000000, 25)
        5000000.0
    """
    if total_amount is None or target_ratio is None:
        return 0.0

    try:
        return total_amount * (target_ratio / 100)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0


def calculate_current_ratio(current_amount: float, total_amount: float) -> float:
    """
    현재 비중을 계산합니다.

    Args:
        current_amount: 현재 금액
        total_amount: 총 투자 금액

    Returns:
        현재 비중 (퍼센트)

    Examples:
        >>> calculate_current_ratio(5000000, 20000000)
        25.0
    """
    if current_amount is None or total_amount is None or total_amount == 0:
        return 0.0

    try:
        return (current_amount / total_amount) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0


def get_color_for_change(value: float) -> str:
    """
    등락률에 따른 색상을 반환합니다.

    Args:
        value: 등락률 (양수: 상승, 음수: 하락, 0: 보합)

    Returns:
        색상 코드

    Examples:
        >>> get_color_for_change(5.67)
        '#00C853'
        >>> get_color_for_change(-2.34)
        '#D32F2F'
    """
    if value is None or value == 0:
        return config.COLOR_NEUTRAL

    return config.COLOR_POSITIVE if value > 0 else config.COLOR_NEGATIVE


def convert_usd_to_krw(usd_amount: float, exchange_rate: float = None) -> float:
    """
    USD를 KRW로 환전합니다.

    Args:
        usd_amount: USD 금액
        exchange_rate: 환율 (None이면 기본 환율 사용)

    Returns:
        KRW 금액

    Examples:
        >>> convert_usd_to_krw(100, 1320)
        132000.0
    """
    if usd_amount is None:
        return 0.0

    if exchange_rate is None:
        exchange_rate = config.DEFAULT_USD_KRW

    try:
        return usd_amount * exchange_rate
    except (ValueError, TypeError):
        return 0.0


def calculate_after_tax_dividend(dividend: float, is_us: bool = False,
                                 use_korea_tax: bool = True) -> float:
    """
    세후 배당금을 계산합니다.

    Args:
        dividend: 배당금 (세전)
        is_us: 미국 주식 여부
        use_korea_tax: 한국 세금 적용 여부

    Returns:
        세후 배당금

    Examples:
        >>> calculate_after_tax_dividend(1000, is_us=True, use_korea_tax=True)
        722.1  # 미국 15% + 한국 14% (분리과세 가정)
        >>> calculate_after_tax_dividend(1000, is_us=False, use_korea_tax=True)
        846.0  # 한국 15.4%
    """
    if dividend is None or dividend == 0:
        return 0.0

    try:
        after_tax = dividend

        # 미국 원천징수세 적용
        if is_us:
            after_tax *= (1 - config.US_WITHHOLDING_TAX)

        # 한국 배당소득세 적용
        if use_korea_tax:
            if is_us:
                # 미국 주식: 원천징수 후 남은 금액에 14% 추가 (분리과세 가정)
                after_tax *= (1 - 0.14)
            else:
                # 한국 주식: 15.4%
                after_tax *= (1 - config.KR_DIVIDEND_TAX)

        return after_tax
    except (ValueError, TypeError):
        return 0.0


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    안전한 나눗셈 (0으로 나누기 방지)

    Args:
        numerator: 분자
        denominator: 분모
        default: 에러 시 반환할 기본값

    Returns:
        나눗셈 결과 또는 기본값
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (ValueError, TypeError, ZeroDivisionError):
        return default
