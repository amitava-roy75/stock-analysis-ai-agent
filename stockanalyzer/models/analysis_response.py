from typing import List
from pydantic import BaseModel, Field


class Metrics(BaseModel):
    """
    Key financial metrics returned to the UI.
    """

    price: str = ""

    marketCap: str = ""

    pe: str = ""

    roe: str = ""

    dividendYield: str = ""


class NewsItem(BaseModel):
    """
    News item displayed on the dashboard.
    """

    title: str

    summary: str = ""

    publisher: str = ""

    published: str = ""

    sentiment: str = ""


class AnalysisResponse(BaseModel):
    """
    Final response returned by /analyze
    """

    query: str

    intent: str

    company: str

    symbol: str

    summary: str

    recommendation: str

    confidence: str

    metrics: Metrics = Field(
        default_factory=Metrics
    )

    news: List[NewsItem] = Field(
        default_factory=list
    )

    report: str