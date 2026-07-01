from config.logging_config import logger

from tools.base_tool import BaseTool
from tools.registry import registry

from services.yahoo_finance_service import yahoo_service


class CompareTool(BaseTool):

    @property
    def name(self):
        return "CompareTool"

    async def execute(self, input_data):
        """
        Collect comparison data for multiple stocks.

        Input

            INFY,TCS
            INFY.NS,TCS.NS
            Infosys,TCS

        Returns

            {
                "responseType": "comparison",
                "stocks": [...]
            }
        """

        try:

            symbols = [

                self.normalize_symbol(symbol.strip())

                for symbol in input_data.split(",")

                if symbol.strip()

            ]

            logger.info(
                "CompareTool Symbols : %s",
                symbols
            )

            stocks = []

            for symbol in symbols:

                logger.info(
                    "Collecting comparison data : %s",
                    symbol
                )

                stock = {

                    "symbol": symbol,

                    "price": await yahoo_service.get_price(symbol),

                    "fundamentals": await yahoo_service.get_fundamentals(symbol),

                    "profile": await yahoo_service.get_profile(symbol)

                }

                stocks.append(stock)

            return {

                "responseType": "comparison",

                "status": "SUCCESS",

                "stocks": stocks

            }

        except Exception as ex:

            logger.exception(ex)

            return {

                "responseType": "comparison",

                "status": "FAILED",

                "message": str(ex),

                "stocks": []

            }


registry.register(CompareTool())