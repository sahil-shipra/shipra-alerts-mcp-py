from mcp.server.fastmcp import FastMCP
from typing import Optional, Literal, List
from apis import create_alert, get_alert_list, get_alert
from create_alert import (
    _dma_condition,
    _drawdown_condition,
    _opportunity_condition,
    _pe_ratio_condition,
    _price_condition,
    _rsi_condition,
)

mcp = FastMCP("shipra")


def main():
    mcp.run(transport="stdio")


@mcp.tool()
async def retrieve_alerts() -> str:
    """Retrieve and return all stock alerts for the user from the Shipra stock platform.

    Returns:
        str: A list of stock alerts for the user.
    """
    res = await get_alert_list()
    return res


@mcp.tool()
async def retrieve_alert(id: str) -> str:
    """Retrieve and return a specific stock alert for the user from the Shipra stock platform.

    Args:
        id (str): Unique identifier of the stock alert.

    Returns:
        str: The stock alert details.
    """
    res = await get_alert(id)
    return res


@mcp.tool()  # RSI
async def create_rsi_alert(
    tickers: List[str],
    rsi_period: int = 14,
    rsi_less_than_x: bool = False,
    rsi_less_than_x_value: float = 30,
    rsi_greater_than_x: bool = False,
    rsi_greater_than_x_value: float = 70,
    rsi_specific_range: bool = False,
    low_range: float = 30,
    high_range: float = 70,
    frequency: Literal["RECURRING", "ONCE"] = "RECURRING",
    expiration_type: Literal["OPEN_ENDED", "DATE"] = "OPEN_ENDED",
    expiration_date: Optional[str] = None,
    notify_email: Optional[str] = None,
) -> dict:
    """
    Create an RSI-based alert for one or more stock tickers.

    Args:
        tickers: List of ticker symbols, e.g. ["AAPL", "TSLA"]
        rsi_period: RSI calculation period (default 14)
        rsi_less_than_x: Trigger when RSI drops below rsi_less_than_x_value
        rsi_less_than_x_value: Threshold for the less-than check (default 30)
        rsi_greater_than_x: Trigger when RSI rises above rsi_greater_than_x_value
        rsi_greater_than_x_value: Threshold for the greater-than check (default 70)
        rsi_specific_range: Trigger when RSI is within [low_range, high_range]
        low_range: Lower bound for range check
        high_range: Upper bound for range check
        frequency: "RECURRING" fires every time, "ONCE" fires only once
        expiration_type: "OPEN_ENDED" has no end, "DATE" expires on expiration_date
        expiration_date: ISO date string, e.g. "2025-12-31" (required if DATE)
        notify_email: Optional email address to receive notifications
    """
    payload = {
        "target": {
            "assetType": "STOCKS",
            "tickers": tickers,
        },
        "conditions": [
            {
                "joinWithNext": None,
                "type": "RSI",
                "condition": _rsi_condition(
                    rsi_period=rsi_period,
                    rsi_less_than_x=rsi_less_than_x,
                    rsi_less_than_x_value=rsi_less_than_x_value,
                    rsi_greater_than_x=rsi_greater_than_x,
                    rsi_greater_than_x_value=rsi_greater_than_x_value,
                    rsi_specific_range=rsi_specific_range,
                    low_range=low_range,
                    high_range=high_range,
                ),
            }
        ],
        "trigger": {"frequency": frequency},
        "expiration": {
            "type": expiration_type,
            **({"date": expiration_date} if expiration_date else {}),
        },
        "notifications": {
            **({"email": {"enabled": True, "addresses": [notify_email]}} if notify_email else {})
        },
    }

    return await create_alert(payload=payload)


@mcp.tool()  # Price
async def create_price_alert(
    tickers: List[str],
    sub_condition: Literal[
        "GOING_UP", "GOING_DOWN",
        "CROSSING_UP", "CROSSING_DOWN",
        "CLOSING_POSITIVE", "CLOSING_NEGATIVE",
    ],
    crossing_up_value: Optional[float] = None,
    crossing_up_type: Optional[Literal["price", "percentage"]] = "price",
    crossing_down_value: Optional[float] = None,
    crossing_down_type: Optional[Literal["price", "percentage"]] = "price",
    nearing_52_week_low: bool = False,
    nearing_52_week_low_value: Optional[float] = None,
    nearing_52_week_high: bool = False,
    nearing_52_week_high_value: Optional[float] = None,
    within_past_x_days: bool = False,
    within_past_x_days_value: Optional[int] = None,
    frequency: Literal["RECURRING", "ONCE"] = "RECURRING",
    expiration_type: Literal["OPEN_ENDED", "DATE"] = "OPEN_ENDED",
    expiration_date: Optional[str] = None,
    notify_email: Optional[str] = None,
    notify_whatsapp: Optional[str] = None,
) -> dict:
    """
    Create a price-based alert for one or more stock tickers.

    Args:
        tickers: List of ticker symbols, e.g. ["AAPL"]
        sub_condition: The price event type:
            GOING_UP / GOING_DOWN      – directional movement
            CROSSING_UP / CROSSING_DOWN – crossing a price or % threshold
            CLOSING_POSITIVE / CLOSING_NEGATIVE – daily close direction
        crossing_up_value: Price/% level to trigger CROSSING_UP
        crossing_up_type: "price" (absolute) or "percentage"
        crossing_down_value: Price/% level to trigger CROSSING_DOWN
        crossing_down_type: "price" or "percentage"
        nearing_52_week_low: Alert when price nears 52-week low
        nearing_52_week_low_value: How close (%) to the 52-week low
        nearing_52_week_high: Alert when price nears 52-week high
        nearing_52_week_high_value: How close (%) to the 52-week high
        within_past_x_days: Filter condition to last X days
        within_past_x_days_value: Number of days
        frequency: "RECURRING" or "ONCE"
        expiration_type: "OPEN_ENDED" or "DATE"
        expiration_date: ISO date if expiration_type is DATE
        notify_email: Optional notification email
        notify_whatsapp: Optional WhatsApp number
    """
    notifications: dict = {}
    if notify_email:
        notifications["email"] = {"enabled": True, "addresses": [notify_email]}
    if notify_whatsapp:
        notifications["whatsapp"] = {
            "enabled": True, "numbers": [notify_whatsapp]}

    payload = {
        "target": {
            "assetType": "STOCKS",
            "tickers": tickers,
        },
        "conditions": [
            {
                "joinWithNext": None,
                "type": "PRICE",
                "condition": _price_condition(
                    sub_condition=sub_condition,
                    crossing_up_value=crossing_up_value,
                    crossing_up_type=crossing_up_type,
                    crossing_down_value=crossing_down_value,
                    crossing_down_type=crossing_down_type,
                    nearing_52_week_low=nearing_52_week_low,
                    nearing_52_week_low_value=nearing_52_week_low_value,
                    nearing_52_week_high=nearing_52_week_high,
                    nearing_52_week_high_value=nearing_52_week_high_value,
                    within_past_x_days=within_past_x_days,
                    within_past_x_days_value=within_past_x_days_value,
                ),
            }
        ],
        "trigger": {"frequency": frequency},
        "expiration": {
            "type": expiration_type,
            **({"date": expiration_date} if expiration_date else {}),
        },
        "notifications": notifications,
    }

    return await create_alert(payload=payload)


@mcp.tool()  # DRAWDOWN
async def create_drawdown_alert(
    tickers: List[str],
    near_last_drawdown: bool = False,
    near_last_drawdown_value: float = 0,
    price_surpass_last_drawdown: bool = False,
    price_surpass_multiple_historical_drawdown: bool = False,
    price_approach_historical_drawdown: bool = False,
    price_approach_historical_drawdown_value: float = 0,
    price_fall_below_historical_drawdown: bool = False,
    price_recover_after_drawdown: bool = False,
    price_recover_after_drawdown_value: float = 0,
    frequency: Literal["RECURRING", "ONCE"] = "RECURRING",
    expiration_type: Literal["OPEN_ENDED", "DATE"] = "OPEN_ENDED",
    expiration_date: Optional[str] = None,
    notify_email: Optional[str] = None,
) -> dict:
    """
    Create a drawdown-based alert.

    Args:
        tickers: List of ticker symbols
        near_last_drawdown: Trigger when price is near the last drawdown
        near_last_drawdown_value: Proximity threshold for near_last_drawdown
        price_surpass_last_drawdown: Trigger when price surpasses the last drawdown
        price_surpass_multiple_historical_drawdown: Trigger when price surpasses multiple historical drawdowns
        price_approach_historical_drawdown: Trigger when price approaches a historical drawdown
        price_approach_historical_drawdown_value: Proximity threshold for historical drawdown approach
        price_fall_below_historical_drawdown: Trigger when price falls below a historical drawdown
        price_recover_after_drawdown: Trigger when price recovers after a drawdown
        price_recover_after_drawdown_value: Recovery threshold after drawdown
        frequency: "RECURRING" or "ONCE"
        expiration_type: "OPEN_ENDED" or "DATE"
        expiration_date: ISO date if expiration_type is DATE
        notify_email: Optional notification email
    """
    payload = {
        "target": {
            "assetType": "STOCKS",
            "tickers": tickers,
        },
        "conditions": [
            {
                "joinWithNext": None,
                "type": "DRAWDOWN",
                "condition": _drawdown_condition(
                    near_last_drawdown=near_last_drawdown,
                    near_last_drawdown_value=near_last_drawdown_value,
                    price_surpass_last_drawdown=price_surpass_last_drawdown,
                    price_surpass_multiple_historical_drawdown=price_surpass_multiple_historical_drawdown,
                    price_approach_historical_drawdown=price_approach_historical_drawdown,
                    price_approach_historical_drawdown_value=price_approach_historical_drawdown_value,
                    price_fall_below_historical_drawdown=price_fall_below_historical_drawdown,
                    price_recover_after_drawdown=price_recover_after_drawdown,
                    price_recover_after_drawdown_value=price_recover_after_drawdown_value,
                ),
            }
        ],
        "trigger": {"frequency": frequency},
        "expiration": {
            "type": expiration_type,
            **({"date": expiration_date} if expiration_date else {}),
        },
        "notifications": {
            **({"email": {"enabled": True, "addresses": [notify_email]}} if notify_email else {})
        },
    }

    return await create_alert(payload=payload)


@mcp.tool()  # DMA
async def create_dma_alert(
    tickers: List[str],
    dma_window: List[int],
    touched_dma: bool = False,
    near_dma: bool = False,
    near_dma_value: float = 0,
    fall_x_from_dma: bool = False,
    fall_x_from_dma_value: float = 0,
    rise_x_from_dma: bool = False,
    rise_x_from_dma_value: float = 0,
    sustain_x_day_above_dma: bool = False,
    sustain_x_day_above_dma_value: int = 0,
    sustain_x_day_below_dma: bool = False,
    sustain_x_day_below_dma_value: int = 0,
    frequency: Literal["RECURRING", "ONCE"] = "RECURRING",
    expiration_type: Literal["OPEN_ENDED", "DATE"] = "OPEN_ENDED",
    expiration_date: Optional[str] = None,
    notify_email: Optional[str] = None,
) -> dict:
    """
    Create a DMA (Daily Moving Average) alert.

    Args:
        tickers: List of ticker symbols
        dma_window: List of DMA periods to watch, e.g. [50, 200]
        touched_dma: Trigger when price touches the DMA
        near_dma: Trigger when price is near the DMA
        near_dma_value: Proximity threshold (%) for near_dma
        fall_x_from_dma: Trigger when price falls X% from DMA
        fall_x_from_dma_value: Fall percentage threshold
        rise_x_from_dma: Trigger when price rises X% from DMA
        rise_x_from_dma_value: Rise percentage threshold
        sustain_x_day_above_dma: Trigger after price sustains above DMA for N days
        sustain_x_day_above_dma_value: Number of consecutive days above
        sustain_x_day_below_dma: Trigger after price sustains below DMA for N days
        sustain_x_day_below_dma_value: Number of consecutive days below
        frequency: "RECURRING" or "ONCE"
        expiration_type: "OPEN_ENDED" or "DATE"
        expiration_date: ISO date if expiration_type is DATE
        notify_email: Optional notification email
    """
    payload = {
        "target": {
            "assetType": "STOCKS",
            "tickers": tickers,
        },
        "conditions": [
            {
                "joinWithNext": None,
                "type": "DMA",
                "condition": _dma_condition(
                    dma_window=dma_window,
                    touched_dma=touched_dma,
                    near_dma=near_dma,
                    near_dma_value=near_dma_value,
                    fall_x_from_dma=fall_x_from_dma,
                    fall_x_from_dma_value=fall_x_from_dma_value,
                    rise_x_from_dma=rise_x_from_dma,
                    rise_x_from_dma_value=rise_x_from_dma_value,
                    sustain_x_day_above_dma=sustain_x_day_above_dma,
                    sustain_x_day_above_dma_value=sustain_x_day_above_dma_value,
                    sustain_x_day_below_dma=sustain_x_day_below_dma,
                    sustain_x_day_below_dma_value=sustain_x_day_below_dma_value,
                ),
            }
        ],
        "trigger": {"frequency": frequency},
        "expiration": {
            "type": expiration_type,
            **({"date": expiration_date} if expiration_date else {}),
        },
        "notifications": {
            **({"email": {"enabled": True, "addresses": [notify_email]}} if notify_email else {})
        },
    }

    return await create_alert(payload=payload)


@mcp.tool()  # PE_RATIO
async def create_pe_alert(
    tickers: List[str],
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
    frequency: Literal["RECURRING", "ONCE"] = "RECURRING",
    expiration_type: Literal["OPEN_ENDED", "DATE"] = "OPEN_ENDED",
    expiration_date: Optional[str] = None,
    notify_email: Optional[str] = None,
) -> dict:
    """
    Create a PE ratio-based alert.

    Args:
        tickers: List of ticker symbols
        pe_ratio_less_than_x: Trigger when PE ratio is below a threshold
        pe_ratio_less_than_x_value: Threshold for pe_ratio_less_than_x
        pe_ratio_greater_than_x: Trigger when PE ratio is above a threshold
        pe_ratio_greater_than_x_value: Threshold for pe_ratio_greater_than_x
        pe_ratio_specific_range: Trigger when PE ratio is within a range
        low_range: Lower bound for the PE ratio range
        high_range: Upper bound for the PE ratio range
        pe_ratio_near_x_year_low: Trigger when PE ratio is near an X-year low
        pe_ratio_near_x_year_low_value: Proximity threshold for X-year low
        pe_ratio_near_x_year_low_year: Number of years for low comparison
        pe_ratio_near_x_year_high: Trigger when PE ratio is near an X-year high
        pe_ratio_near_x_year_high_value: Proximity threshold for X-year high
        pe_ratio_near_x_year_high_year: Number of years for high comparison
        pe_ratio_historical_extreme: Trigger when PE ratio hits a historical extreme
        pe_ratio_trending_up: Trigger when PE ratio is trending up
        pe_ratio_trending_up_value: Trend threshold for upward movement
        pe_ratio_trending_down: Trigger when PE ratio is trending down
        pe_ratio_trending_down_value: Trend threshold for downward movement
        frequency: "RECURRING" or "ONCE"
        expiration_type: "OPEN_ENDED" or "DATE"
        expiration_date: ISO date if expiration_type is DATE
        notify_email: Optional notification email
    """
    payload = {
        "target": {
            "assetType": "STOCKS",
            "tickers": tickers,
        },
        "conditions": [
            {
                "joinWithNext": None,
                "type": "PE_RATIO",
                "condition": _pe_ratio_condition(
                    pe_ratio_less_than_x=pe_ratio_less_than_x,
                    pe_ratio_less_than_x_value=pe_ratio_less_than_x_value,
                    pe_ratio_greater_than_x=pe_ratio_greater_than_x,
                    pe_ratio_greater_than_x_value=pe_ratio_greater_than_x_value,
                    pe_ratio_specific_range=pe_ratio_specific_range,
                    low_range=low_range,
                    high_range=high_range,
                    pe_ratio_near_x_year_low=pe_ratio_near_x_year_low,
                    pe_ratio_near_x_year_low_value=pe_ratio_near_x_year_low_value,
                    pe_ratio_near_x_year_low_year=pe_ratio_near_x_year_low_year,
                    pe_ratio_near_x_year_high=pe_ratio_near_x_year_high,
                    pe_ratio_near_x_year_high_value=pe_ratio_near_x_year_high_value,
                    pe_ratio_near_x_year_high_year=pe_ratio_near_x_year_high_year,
                    pe_ratio_historical_extreme=pe_ratio_historical_extreme,
                    pe_ratio_trending_up=pe_ratio_trending_up,
                    pe_ratio_trending_up_value=pe_ratio_trending_up_value,
                    pe_ratio_trending_down=pe_ratio_trending_down,
                    pe_ratio_trending_down_value=pe_ratio_trending_down_value,
                ),
            }
        ],
        "trigger": {"frequency": frequency},
        "expiration": {
            "type": expiration_type,
            **({"date": expiration_date} if expiration_date else {}),
        },
        "notifications": {
            **({"email": {"enabled": True, "addresses": [notify_email]}} if notify_email else {})
        },
    }

    return await create_alert(payload=payload)


@mcp.tool()  # OPPORTUNITY
async def create_opportunity_alert(
    tickers: List[str],
    value: float,
    sub_condition: Literal["GOING_UP", "GOING_DOWN"],
    frequency: Literal["RECURRING", "ONCE"] = "RECURRING",
    expiration_type: Literal["OPEN_ENDED", "DATE"] = "OPEN_ENDED",
    expiration_date: Optional[str] = None,
    notify_email: Optional[str] = None,
) -> dict:
    """
    Create an opportunity-based alert.

    Args:
        tickers: List of ticker symbols
        value: Numeric threshold for the opportunity condition
        sub_condition: Direction of the opportunity signal, "GOING_UP" or "GOING_DOWN"
        frequency: "RECURRING" or "ONCE"
        expiration_type: "OPEN_ENDED" or "DATE"
        expiration_date: ISO date if expiration_type is DATE
        notify_email: Optional notification email
    """
    payload = {
        "target": {
            "assetType": "STOCKS",
            "tickers": tickers,
        },
        "conditions": [
            {
                "joinWithNext": None,
                "type": "OPPORTUNITY",
                "condition": _opportunity_condition(
                    value=value,
                    sub_condition=sub_condition,
                ),
            }
        ],
        "trigger": {"frequency": frequency},
        "expiration": {
            "type": expiration_type,
            **({"date": expiration_date} if expiration_date else {}),
        },
        "notifications": {
            **({"email": {"enabled": True, "addresses": [notify_email]}} if notify_email else {})
        },
    }

    return await create_alert(payload=payload)


# @mcp.tool()
# async def create_alert_raw(
#     target_asset_type: Literal["STOCKS", "WATCHLIST"],
#     tickers: List[str],
#     condition_type: Literal["RSI", "PRICE", "DRAWDOWN", "PE_RATIO", "OPPORTUNITY", "DMA"],
#     condition: dict,
#     frequency: Literal["RECURRING", "ONCE"] = "RECURRING",
#     expiration_type: Literal["OPEN_ENDED", "DATE"] = "OPEN_ENDED",
#     expiration_date: Optional[str] = None,
#     join_with_next: Optional[Literal["AND", "OR"]] = None,
#     notify_email: Optional[str] = None,
#     notify_whatsapp: Optional[str] = None,
#     watchlist_ids: Optional[List[str]] = None,
# ) -> dict:
#     """
#     Create any type of alert by passing the condition dict directly.
#     Use this for DRAWDOWN, PE_RATIO, OPPORTUNITY conditions or for
#     complex multi-condition payloads.

#     Args:
#         target_asset_type: "STOCKS" or "WATCHLIST"
#         tickers: Ticker symbols (required even for WATCHLIST)
#         condition_type: One of RSI | PRICE | DRAWDOWN | PE_RATIO | OPPORTUNITY | DMA
#         condition: The raw condition object matching the corresponding DTO
#         frequency: "RECURRING" or "ONCE"
#         expiration_type: "OPEN_ENDED" or "DATE"
#         expiration_date: ISO date string if expiration_type is DATE
#         join_with_next: "AND" / "OR" for chaining multiple conditions (leave None for single)
#         notify_email: Optional email for notifications
#         notify_whatsapp: Optional WhatsApp number
#         watchlist_ids: Watchlist IDs when assetType is WATCHLIST
#     """
#     notifications: dict = {}
#     if notify_email:
#         notifications["email"] = {"enabled": True, "addresses": [notify_email]}
#     if notify_whatsapp:
#         notifications["whatsapp"] = {
#             "enabled": True, "numbers": [notify_whatsapp]}

#     target: dict = {"assetType": target_asset_type, "tickers": tickers}
#     if watchlist_ids:
#         target["watchlistIds"] = watchlist_ids

#     payload = {
#         "target": target,
#         "conditions": [
#             {
#                 "joinWithNext": join_with_next,
#                 "type": condition_type,
#                 "condition": condition,
#             }
#         ],
#         "trigger": {"frequency": frequency},
#         "expiration": {
#             "type": expiration_type,
#             **({"date": expiration_date} if expiration_date else {}),
#         },
#         "notifications": notifications,
#     }

#     return await create_alert(payload=payload)


if __name__ == "__main__":
    main()
