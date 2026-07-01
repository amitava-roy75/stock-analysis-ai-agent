from config.logging_config import logger

from tools.base_tool import BaseTool
from tools.registry import registry

from services.yahoo_finance_service import yahoo_service


class NewsTool(BaseTool):

    @property
    def name(self):
        return "NewsTool"

    async def execute(self, input_data):
        """
        Retrieves latest company news.

        Supported Inputs

            Infosys
            INFY
            INFY.NS
            TCS
            RELIANCE
            AAPL
            MSFT
        """

        try:

            #
            # Resolve to Yahoo Finance Symbol
            #

            symbol = self.normalize_symbol(input_data)

            logger.info(
                "NewsTool : %s -> %s",
                input_data,
                symbol
            )

            news = await yahoo_service.get_news(symbol)

            #
            # Return top 10 news
            #

            return news[:10]

        except Exception as ex:

            logger.exception(ex)

            return {

                "status": "FAILED",

                "message": str(ex)

            }


registry.register(NewsTool())