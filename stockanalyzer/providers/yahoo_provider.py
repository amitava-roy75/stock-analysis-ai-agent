import yfinance as yf

from providers.base_provider import BaseProvider


class YahooProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "Yahoo Finance"

    def safe(self, value, default="N/A"):
        """Return the default value if the supplied value is None."""
        return default if value is None else value

    async def get_price(self, symbol: str):
        ticker = yf.Ticker(symbol)

        info = ticker.info
        fast = ticker.fast_info
        history = ticker.history(period="2d", auto_adjust=False)

        current_price = (
            fast.get("lastPrice")
            or info.get("currentPrice")
        )

        if current_price is None and not history.empty:
            current_price = float(history["Close"].iloc[-1])

        previous_close = (
            fast.get("previousClose")
            or info.get("previousClose")
        )

        if previous_close is None and len(history) > 1:
            previous_close = float(history["Close"].iloc[-2])

        return {
            "symbol": symbol,
            "price": self.safe(current_price, 0.0),
            "previousClose": self.safe(previous_close, 0.0),
            "open": self.safe(
                fast.get("open") or info.get("open"),
                0.0,
            ),
            "dayHigh": self.safe(
                fast.get("dayHigh") or info.get("dayHigh"),
                0.0,
            ),
            "dayLow": self.safe(
                fast.get("dayLow") or info.get("dayLow"),
                0.0,
            ),
            "volume": self.safe(
                fast.get("lastVolume") or info.get("volume"),
                0,
            ),
            "currency": self.safe(
                info.get("currency"),
                "INR" if symbol.endswith(".NS") else "USD",
            ),
            "exchange": self.safe(
                info.get("exchange"),
                "NSE" if symbol.endswith(".NS") else "NASDAQ",
            ),
        }

    async def get_news(self, symbol: str):
        ticker = yf.Ticker(symbol)

        try:
            return ticker.news[:10]
        except Exception:
            return []

    async def get_fundamentals(self, symbol: str):
        ticker = yf.Ticker(symbol)

        info = ticker.info
        fast = ticker.fast_info

        return {
            "symbol": symbol,
            "currentPrice": self.safe(
                fast.get("lastPrice") or info.get("currentPrice"),
                0.0,
            ),
            "previousClose": self.safe(
                fast.get("previousClose") or info.get("previousClose"),
                0.0,
            ),
            "marketCap": self.safe(
                info.get("marketCap"),
                0,
            ),
            "enterpriseValue": self.safe(
                info.get("enterpriseValue"),
                0,
            ),
            "trailingPE": self.safe(
                info.get("trailingPE") or info.get("currentPE"),
                0.0,
            ),
            "forwardPE": self.safe(
                info.get("forwardPE"),
                0.0,
            ),
            "priceToBook": self.safe(
                info.get("priceToBook"),
                0.0,
            ),
            "bookValue": self.safe(
                info.get("bookValue"),
                0.0,
            ),
            "eps": self.safe(
                info.get("trailingEps") or info.get("epsTrailingTwelveMonths"),
                0.0,
            ),
            "beta": self.safe(
                info.get("beta"),
                0.0,
            ),
            "dividendYield": self.safe(
                info.get("dividendYield"),
                0.0,
            ),
            "profitMargins": self.safe(
                info.get("profitMargins"),
                0.0,
            ),
            "operatingMargins": self.safe(
                info.get("operatingMargins"),
                0.0,
            ),
            "returnOnEquity": self.safe(
                info.get("returnOnEquity"),
                0.0,
            ),
            "returnOnAssets": self.safe(
                info.get("returnOnAssets"),
                0.0,
            ),
            "revenueGrowth": self.safe(
                info.get("revenueGrowth"),
                0.0,
            ),
            "earningsGrowth": self.safe(
                info.get("earningsGrowth"),
                0.0,
            ),
            "averageVolume": self.safe(
                fast.get("tenDayAverageVolume") or info.get("averageVolume"),
                0,
            ),
            "currency": self.safe(
                info.get("currency"),
                "INR" if symbol.endswith(".NS") else "USD",
            ),
        }

    async def get_profile(self, symbol: str):
        ticker = yf.Ticker(symbol)
        info = ticker.info

        return {
            "symbol": symbol,
            "company": info.get("longName"),
            "shortName": info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "country": info.get("country"),
            "website": info.get("website"),
            "employees": info.get("fullTimeEmployees"),
            "businessSummary": info.get("longBusinessSummary"),
        }

    async def get_financials(self, symbol: str):
        ticker = yf.Ticker(symbol)
        result = {}

        try:
            if hasattr(ticker, "income_stmt") and ticker.income_stmt is not None:
                if not ticker.income_stmt.empty:
                    result["incomeStatement"] = (
                        ticker.income_stmt.fillna("").to_dict()
                    )
        except Exception:
            result["incomeStatement"] = {}

        try:
            if hasattr(ticker, "balance_sheet") and ticker.balance_sheet is not None:
                if not ticker.balance_sheet.empty:
                    result["balanceSheet"] = (
                        ticker.balance_sheet.fillna("").to_dict()
                    )
        except Exception:
            result["balanceSheet"] = {}

        try:
            if hasattr(ticker, "cashflow") and ticker.cashflow is not None:
                if not ticker.cashflow.empty:
                    result["cashFlow"] = (
                        ticker.cashflow.fillna("").to_dict()
                    )
        except Exception:
            result["cashFlow"] = {}

        return result
