from tools.base_tool import BaseTool
from tools.registry import registry
from services.yahoo_finance_service import yahoo_service


class CompanyProfileTool(BaseTool):

    @property
    def name(self):
        return "CompanyProfileTool"

    async def execute(self, input_data):

        return await yahoo_service.get_profile(
            input_data
        )


registry.register(CompanyProfileTool())