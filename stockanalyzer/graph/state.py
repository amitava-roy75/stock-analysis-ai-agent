from typing import Any, TypedDict


class StockState(TypedDict):

    query: str

    intent: str

    company: str

    symbol: str

    plan: dict

    tool_results: list[Any]

    messages: list[str]

    final_answer: str