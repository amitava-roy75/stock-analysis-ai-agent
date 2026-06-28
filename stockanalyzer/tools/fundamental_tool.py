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

        Args:
            input_data (str): Stock symbol
                Examples:
                    RELIANCE.NS
                    TCS.NS
                    INFY.NS
                    AAPL
                    MSFT
        """

        try:
            result = await yahoo_service.get_fundamentals(input_data)
            return result

        except Exception as e:
            return {
                "status": "FAILED",
                "message": str(e)
            }


registry.register(FundamentalTool())