from config.logging_config import logger

from tools.base_tool import BaseTool
from tools.registry import registry

from services.yahoo_finance_service import yahoo_service


class FundamentalTool(BaseTool):

    @property
    def name(self):
        return "FundamentalTool"

    async def execute(self, input_data):
        """
        Retrieves company fundamentals.

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
                "FundamentalTool : %s -> %s",
                input_data,
                symbol
            )

            result = await yahoo_service.get_fundamentals(symbol)

            return result

        except Exception as ex:

            logger.exception(ex)

            return {

                "status": "FAILED",

                "message": str(ex)

            }


registry.register(FundamentalTool())