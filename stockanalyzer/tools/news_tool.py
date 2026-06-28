from tools.base_tool import BaseTool
from tools.registry import registry
from services.yahoo_finance_service import yahoo_service


class NewsTool(BaseTool):

    @property
    def name(self):
        return "NewsTool"

    async def execute(self, input_data):

        news = await yahoo_service.get_news(
            input_data
        )

        return news[:10]


registry.register(NewsTool())