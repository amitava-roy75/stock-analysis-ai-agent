from fastapi import APIRouter, HTTPException

from tools.registry import registry

router = APIRouter(
    tags=["Stock APIs"]
)


def get_tool(name: str):
    tool = registry.get(name)

    if tool is None:
        raise HTTPException(
            status_code=404,
            detail=f"{name} not registered"
        )

    return tool


@router.get("/price")
async def get_price(symbol: str):

    tool = get_tool("PriceTool")

    return await tool.execute(symbol)


@router.get("/fundamental")
async def get_fundamental(symbol: str):

    tool = get_tool("FundamentalTool")

    return await tool.execute(symbol)


@router.get("/news")
async def get_news(symbol: str):

    tool = get_tool("NewsTool")

    return await tool.execute(symbol)


@router.get("/profile")
async def get_profile(symbol: str):

    tool = get_tool("CompanyProfileTool")

    return await tool.execute(symbol)


@router.get("/financials")
async def get_financials(symbol: str):

    tool = get_tool("FinancialStatementTool")

    return await tool.execute(symbol)


@router.get("/compare")
async def compare(symbols: str):

    tool = get_tool("CompareTool")

    return await tool.execute(symbols)