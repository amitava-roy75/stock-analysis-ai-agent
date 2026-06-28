from providers.provider_factory import ProviderFactory


class YahooFinanceService:

    def __init__(self):
        self.provider = ProviderFactory.provider()

    async def get_price(self, symbol: str):
        return await self.provider.get_price(symbol)

    async def get_news(self, symbol: str):
        return await self.provider.get_news(symbol)

    async def get_fundamentals(self, symbol: str):
        return await self.provider.get_fundamentals(symbol)

    async def get_profile(self, symbol: str):
        return await self.provider.get_profile(symbol)

    async def get_financials(self, symbol: str):
        return await self.provider.get_financials(symbol)


yahoo_service = YahooFinanceService()