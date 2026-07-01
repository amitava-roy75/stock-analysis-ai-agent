from config.logging_config import logger

from tools.base_tool import BaseTool
from tools.registry import registry

from services.yahoo_finance_service import yahoo_service


class CompanyProfileTool(BaseTool):

    @property
    def name(self):
        return "CompanyProfileTool"

    async def execute(self, input_data):
        """
        Retrieves company profile information.

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
                "CompanyProfileTool : %s -> %s",
                input_data,
                symbol
            )

            return await yahoo_service.get_profile(symbol)

        except Exception as ex:

            logger.exception(ex)

            return {

                "status": "FAILED",

                "message": str(ex)

            }


registry.register(CompanyProfileTool())