from providers.yahoo_provider import YahooProvider


class ProviderFactory:

    _provider = YahooProvider()

    @classmethod
    def provider(cls):
        return cls._provider