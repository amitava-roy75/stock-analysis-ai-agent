import pandas as pd
import yfinance as yf

from config.logging_config import logger


class PriceHistoryTool:
    """
    Returns historical stock prices.

    Used by

    - Stock Chart
    - Technical Indicators
    - Trend Analysis
    """

    async def execute(
        self,
        symbol: str,
        period: str = "1y"
    ):

        logger.info(
            "PriceHistoryTool : %s (%s)",
            symbol,
            period
        )

        try:

            ticker = yf.Ticker(symbol)

            hist = ticker.history(
                period=period,
                auto_adjust=False
            )

            if hist.empty:

                return {
                    "success": False,
                    "message": "No historical price found.",
                    "data": []
                }

            hist = hist.reset_index()

            data = []

            for _, row in hist.iterrows():

                data.append({

                    "date": row["Date"].strftime("%Y-%m-%d"),

                    "open": round(float(row["Open"]), 2),

                    "high": round(float(row["High"]), 2),

                    "low": round(float(row["Low"]), 2),

                    "close": round(float(row["Close"]), 2),

                    "volume": int(row["Volume"])

                })

            return {

                "success": True,

                "symbol": symbol,

                "period": period,

                "count": len(data),

                "data": data

            }

        except Exception as ex:

            logger.exception(ex)

            return {

                "success": False,

                "message": str(ex),

                "data": []

            }


price_history_tool = PriceHistoryTool()