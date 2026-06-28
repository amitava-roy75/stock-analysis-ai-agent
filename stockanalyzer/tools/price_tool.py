from tools.base_tool import BaseTool
from tools.registry import registry
from services.yahoo_finance_service import yahoo_service


class PriceTool(BaseTool):

    @property
    def name(self):
        return "PriceTool"

    async def execute(self, input_data):
        """
        Retrieves the latest stock price.

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
            result = await yahoo_service.get_price(input_data)
            return result

        except Exception as e:
            return {
                "status": "FAILED",
                "message": str(e)
            }


registry.register(PriceTool())