from abc import ABC, abstractmethod

from services.symbol_resolver import symbol_resolver


class BaseTool(ABC):
    """
    Base class for all tools.

    Responsibilities

    - Common interface
    - Symbol normalization
    - Future retry support
    - Future metrics support
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Tool name registered in ToolRegistry.
        """
        pass

    @abstractmethod
    async def execute(self, input_data):
        """
        Execute the tool.
        """
        pass

    #
    # ----------------------------------------------------------
    # Common Helper
    # ----------------------------------------------------------
    #

    def normalize_symbol(self, symbol: str) -> str:
        """
        Resolve company name / ticker into Yahoo Finance symbol.

        Examples

            Infosys -> INFY.NS
            INFY -> INFY.NS
            TCS -> TCS.NS
        """

        return symbol_resolver.resolve(symbol)