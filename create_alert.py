from mcp.server.fastmcp import FastMCP
from typing import Optional, Literal, List
mcp = FastMCP("shipra")

# ---------------------------------------------------------------------------
# Configuration  – override via environment variables
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Helper: condition builders
# ---------------------------------------------------------------------------

def _rsi_condition(
    rsi_period: int = 14,
    rsi_less_than_x: bool = False,
    rsi_less_than_x_value: float = 30,
    rsi_greater_than_x: bool = False,
    rsi_greater_than_x_value: float = 70,
    rsi_specific_range: bool = False,
    low_range: float = 30,
    high_range: float = 70,
    rsi_historical_low_extreme: bool = False,
    rsi_historical_low_extreme_value: float = 20,
    rsi_historical_high_extreme: bool = False,
    rsi_historical_high_extreme_value: float = 80,
) -> dict:
    return {
        "rsiPeriod": rsi_period,
        "rsiLessThanX": rsi_less_than_x,
        "rsiLessThanXValue": rsi_less_than_x_value,
        "rsiGreaterThanX": rsi_greater_than_x,
        "rsiGreaterThanXValue": rsi_greater_than_x_value,
        "rsiSpecificRange": rsi_specific_range,
        "lowRange": low_range,
        "highRange": high_range,
        "rsiHistoricalLowExtreme": rsi_historical_low_extreme,
        "rsiHistoricalLowExtremeValue": rsi_historical_low_extreme_value,
        "rsiHistoricalHighExtreme": rsi_historical_high_extreme,
        "rsiHistoricalHighExtremeValue": rsi_historical_high_extreme_value,
    }


def _price_condition(
    sub_condition: Literal[
        "GOING_UP", "GOING_DOWN",
        "CROSSING_UP", "CROSSING_DOWN",
        "CLOSING_POSITIVE", "CLOSING_NEGATIVE",
    ],
    # advance condition fields (all optional)
    from_today_open_price: bool = False,
    from_today_open_price_type: Optional[Literal["price",
                                                 "percentage"]] = None,
    from_today_open_price_value: Optional[float] = None,
    crossing_up_type: Optional[Literal["price", "percentage"]] = None,
    crossing_up_value: Optional[float] = None,
    crossing_down_type: Optional[Literal["price", "percentage"]] = None,
    crossing_down_value: Optional[float] = None,
    within_past_x_days: bool = False,
    within_past_x_days_value: Optional[int] = None,
    nearing_52_week_low: bool = False,
    nearing_52_week_low_value: Optional[float] = None,
    nearing_52_week_high: bool = False,
    nearing_52_week_high_value: Optional[float] = None,
) -> dict:
    advance: dict = {}
    if from_today_open_price:
        advance["fromTodayOpenPrice"] = True
        if from_today_open_price_type:
            advance["fromTodayOpenPriceType"] = from_today_open_price_type
        if from_today_open_price_value is not None:
            advance["fromTodayOpenPriceValue"] = from_today_open_price_value
    if crossing_up_value is not None:
        advance["crossingUpType"] = crossing_up_type or "price"
        advance["crossingUpValue"] = crossing_up_value
    if crossing_down_value is not None:
        advance["crossingDownType"] = crossing_down_type or "price"
        advance["crossingDownValue"] = crossing_down_value
    if within_past_x_days:
        advance["withinPastXDays"] = True
        if within_past_x_days_value is not None:
            advance["withinPastXDaysValue"] = within_past_x_days_value
    if nearing_52_week_low:
        advance["nearing52WeekLow"] = True
        if nearing_52_week_low_value is not None:
            advance["nearing52WeekLowValue"] = nearing_52_week_low_value
    if nearing_52_week_high:
        advance["nearing52WeekHigh"] = True
        if nearing_52_week_high_value is not None:
            advance["nearing52WeekHighValue"] = nearing_52_week_high_value

    return {"subCondition": sub_condition, "advanceCondition": advance}


def _dma_condition(
    dma_window: Optional[List[int]] = None,
    touched_dma: bool = False,
    touched_dma_value: float = 200,
    fall_x_from_dma: bool = False,
    fall_x_from_dma_value: float = 0,
    rise_x_from_dma: bool = False,
    rise_x_from_dma_value: float = 0,
    near_dma: bool = False,
    near_dma_value: float = 0,
    sustain_x_day_above_dma: bool = False,
    sustain_x_day_above_dma_value: int = 0,
    sustain_x_day_below_dma: bool = False,
    sustain_x_day_below_dma_value: int = 0,
) -> dict:
    return {
        "dmaWindow": dma_window or [200],
        "touchedDma": touched_dma,
        "touchedDmaValue": touched_dma_value,
        "fallXFromDma": fall_x_from_dma,
        "fallXFromDmaValue": fall_x_from_dma_value,
        "riseXFromDma": rise_x_from_dma,
        "riseXFromDmaValue": rise_x_from_dma_value,
        "nearDma": near_dma,
        "nearDmaValue": near_dma_value,
        "sustainXDayAboveDma": sustain_x_day_above_dma,
        "sustainXDayAboveDmaValue": sustain_x_day_above_dma_value,
        "sustainXDayBelowDma": sustain_x_day_below_dma,
        "sustainXDayBelowDmaValue": sustain_x_day_below_dma_value,
    }


def _drawdown_condition(
    near_last_drawdown: bool = False,
    near_last_drawdown_value: float = 0,
    price_surpass_last_drawdown: bool = False,
    price_surpass_multiple_historical_drawdown: bool = False,
    price_approach_historical_drawdown: bool = False,
    price_approach_historical_drawdown_value: float = 0,
    price_fall_below_historical_drawdown: bool = False,
    price_recover_after_drawdown: bool = False,
    price_recover_after_drawdown_value: float = 0,
) -> dict:
    return {
        "nearLastDrawdown": near_last_drawdown,
        "nearLastDrawdownValue": near_last_drawdown_value,
        "priceSurpassLastDrawdown": price_surpass_last_drawdown,
        "priceSurpassMultipleHistoricalDrawdown": price_surpass_multiple_historical_drawdown,
        "priceApproachHistoricalDrawdown": price_approach_historical_drawdown,
        "priceApproachHistoricalDrawdownValue": price_approach_historical_drawdown_value,
        "priceFallBelowHistoricalDrawdown": price_fall_below_historical_drawdown,
        "priceRecoverAfterDrawdown": price_recover_after_drawdown,
        "priceRecoverAfterDrawdownValue": price_recover_after_drawdown_value,
    }


def _pe_ratio_condition(
    pe_ratio_less_than_x: bool = False,
    pe_ratio_less_than_x_value: float = 0,
    pe_ratio_greater_than_x: bool = False,
    pe_ratio_greater_than_x_value: float = 0,
    pe_ratio_specific_range: bool = False,
    low_range: float = 0,
    high_range: float = 0,
    pe_ratio_near_x_year_low: bool = False,
    pe_ratio_near_x_year_low_value: float = 0,
    pe_ratio_near_x_year_low_year: int = 0,
    pe_ratio_near_x_year_high: bool = False,
    pe_ratio_near_x_year_high_value: float = 0,
    pe_ratio_near_x_year_high_year: int = 0,
    pe_ratio_historical_extreme: bool = False,
    pe_ratio_trending_up: bool = False,
    pe_ratio_trending_up_value: float = 0,
    pe_ratio_trending_down: bool = False,
    pe_ratio_trending_down_value: float = 0,
) -> dict:
    return {
        "peRatioLessThanX": pe_ratio_less_than_x,
        "peRatioLessThanXValue": pe_ratio_less_than_x_value,
        "peRatioGreaterThanX": pe_ratio_greater_than_x,
        "peRatioGreaterThanXValue": pe_ratio_greater_than_x_value,
        "peRatioSpecificRange": pe_ratio_specific_range,
        "lowRange": low_range,
        "highRange": high_range,
        "peRatioNearXYearLow": pe_ratio_near_x_year_low,
        "peRatioNearXYearLowValue": pe_ratio_near_x_year_low_value,
        "peRatioNearXYearLowYear": pe_ratio_near_x_year_low_year,
        "peRatioNearXYearHigh": pe_ratio_near_x_year_high,
        "peRatioNearXYearHighValue": pe_ratio_near_x_year_high_value,
        "peRatioNearXYearHighYear": pe_ratio_near_x_year_high_year,
        "peRatioHistoricalExtreme": pe_ratio_historical_extreme,
        "peRatioTrendingUp": pe_ratio_trending_up,
        "peRatioTrendingUpValue": pe_ratio_trending_up_value,
        "peRatioTrendingDown": pe_ratio_trending_down,
        "peRatioTrendingDownValue": pe_ratio_trending_down_value,
    }


def _opportunity_condition(
    value: float,
    sub_condition: Literal["GOING_UP", "GOING_DOWN"],
) -> dict:
    return {
        "value": value,
        "subCondition": sub_condition,
    }
