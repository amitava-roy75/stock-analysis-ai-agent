from tools.base_tool import BaseTool
from tools.registry import registry
from services.yahoo_finance_service import yahoo_service


class FinancialStatementTool(BaseTool):

    @property
    def name(self):
        return "FinancialStatementTool"

    async def execute(self, input_data):

        return await yahoo_service.get_financials(
            input_data
        )


registry.register(FinancialStatementTool())