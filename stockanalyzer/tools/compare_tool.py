from tools.base_tool import BaseTool
from tools.registry import registry
from services.yahoo_finance_service import yahoo_service


class CompareTool(BaseTool):

    @property
    def name(self):
        return "CompareTool"

    async def execute(self, input_data):

        symbols = [
            s.strip()
            for s in input_data.split(",")
        ]

        comparison = []

        for symbol in symbols:

            price = await yahoo_service.get_price(
                symbol
            )

            fundamentals = await yahoo_service.get_fundamentals(
                symbol
            )

            comparison.append({

                "symbol": symbol,

                "price": price,

                "marketCap": fundamentals.get("marketCap"),

                "peRatio": fundamentals.get("trailingPE")

            })

        return comparison


registry.register(CompareTool())