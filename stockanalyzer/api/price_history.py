from fastapi import APIRouter, HTTPException

from config.logging_config import logger
from tools.price_history_tool import price_history_tool

router = APIRouter(
    prefix="",
    tags=["Market Data"]
)


@router.get("/price-history")
async def get_price_history(
    symbol: str,
    period: str = "1y"
):
    """
    Returns historical stock prices.

    Supported periods

    1d
    5d
    1mo
    3mo
    6mo
    1y
    2y
    5y
    max
    """

    try:

        logger.info("==============================")
        logger.info("Price History API")
        logger.info("Symbol : %s", symbol)
        logger.info("Period : %s", period)
        logger.info("==============================")

        result = await price_history_tool.execute(
            symbol=symbol,
            period=period
        )

        return result

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )