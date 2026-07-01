from typing import Any, TypedDict


class StockState(TypedDict):

    #
    # User Request
    #

    query: str

    intent: str

    company: str

    symbol: str

    #
    # Planner
    #

    plan: dict

    #
    # Router / Tool Execution
    #

    tool_results: list[Any]

    #
    # Conversation
    #

    messages: list[Any]

    #
    # Analysis
    #

    summary: str

    recommendation: str

    confidence: str

    metrics: dict[str, Any]

    news: list[dict[str, Any]]

    #
    # Knowledge
    #

    knowledge: str

    #
    # Compare
    #

    comparison: dict[str, Any]

    #
    # Final Response
    #

    final_answer: str