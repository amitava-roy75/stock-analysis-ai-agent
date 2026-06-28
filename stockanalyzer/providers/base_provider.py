from abc import ABC, abstractmethod
from typing import Any


class BaseProvider(ABC):
    """
    Base interface for all market data providers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Provider name.
        """
        pass

    @abstractmethod
    async def get_price(
        self,
        symbol: str
    ) -> Any:
        pass

    @abstractmethod
    async def get_news(
        self,
        symbol: str
    ) -> Any:
        pass

    @abstractmethod
    async def get_fundamentals(
        self,
        symbol: str
    ) -> Any:
        pass

    @abstractmethod
    async def get_profile(
        self,
        symbol: str
    ) -> Any:
        pass

    @abstractmethod
    async def get_financials(
        self,
        symbol: str
    ) -> Any:
        pass