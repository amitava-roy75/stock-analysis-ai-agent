from config.logging_config import logger


class SymbolResolver:
    """
    Resolves user-provided company names or stock symbols
    to Yahoo Finance symbols.

    Examples
    --------
    Infosys        -> INFY.NS
    INFY           -> INFY.NS
    TCS            -> TCS.NS
    Reliance       -> RELIANCE.NS
    HDFC Bank      -> HDFCBANK.NS
    """

    SYMBOL_MAP = {

        # IT

        "INFY": "INFY.NS",
        "INFOSYS": "INFY.NS",

        "TCS": "TCS.NS",
        "TATA CONSULTANCY SERVICES": "TCS.NS",

        "WIPRO": "WIPRO.NS",

        "HCL": "HCLTECH.NS",
        "HCLTECH": "HCLTECH.NS",
        "HCL TECHNOLOGIES": "HCLTECH.NS",

        "TECHM": "TECHM.NS",
        "TECH MAHINDRA": "TECHM.NS",

        # Banking

        "HDFCBANK": "HDFCBANK.NS",
        "HDFC BANK": "HDFCBANK.NS",

        "ICICI": "ICICIBANK.NS",
        "ICICI BANK": "ICICIBANK.NS",

        "SBI": "SBIN.NS",
        "STATE BANK OF INDIA": "SBIN.NS",

        "AXIS": "AXISBANK.NS",
        "AXIS BANK": "AXISBANK.NS",

        "KOTAK": "KOTAKBANK.NS",
        "KOTAK BANK": "KOTAKBANK.NS",

        # Energy

        "RELIANCE": "RELIANCE.NS",

        "ONGC": "ONGC.NS",

        # Auto

        "MARUTI": "MARUTI.NS",
        "MARUTI SUZUKI": "MARUTI.NS",

        "TATAMOTORS": "TATAMOTORS.NS",
        "TATA MOTORS": "TATAMOTORS.NS",

        "M&M": "M&M.NS",
        "MAHINDRA": "M&M.NS",

        # FMCG

        "HINDUNILVR": "HINDUNILVR.NS",
        "HUL": "HINDUNILVR.NS",

        "ITC": "ITC.NS",

        # Telecom

        "BHARTI": "BHARTIARTL.NS",
        "AIRTEL": "BHARTIARTL.NS",
        "BHARTI AIRTEL": "BHARTIARTL.NS"

    }

    def resolve(self, symbol: str) -> str:

        if not symbol:
            return symbol

        key = symbol.strip().upper()

        #
        # Already Yahoo format
        #

        if key.endswith(".NS"):

            return key

        #
        # Lookup
        #

        resolved = self.SYMBOL_MAP.get(key)

        if resolved:

            logger.info(
                "Resolved %s -> %s",
                key,
                resolved
            )

            return resolved

        #
        # Default
        #

        logger.info(
            "No mapping found for %s. Using as-is.",
            key
        )

        return key


symbol_resolver = SymbolResolver()