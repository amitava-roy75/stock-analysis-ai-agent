from fastapi import APIRouter, HTTPException

from config.logging_config import logger
from tools.company_profile_tool import CompanyProfileTool

router = APIRouter(
    prefix="",
    tags=["Company"]
)


@router.get("/company")
async def get_company(symbol: str):

    try:

        logger.info("===============================")
        logger.info("Company Snapshot API")
        logger.info("Symbol : %s", symbol)
        logger.info("===============================")

        tool = CompanyProfileTool()

        result = await tool.execute(symbol)

        if not result:

            return {}

        return {

            "symbol": symbol,

            "company": result.get(
                "longName",
                result.get("shortName", "")
            ),

            "sector": result.get(
                "sector",
                "Not Available"
            ),

            "industry": result.get(
                "industry",
                "Not Available"
            ),

            "country": result.get(
                "country",
                "Not Available"
            ),

            "city": result.get(
                "city",
                "Not Available"
            ),

            "employees": result.get(
                "fullTimeEmployees",
                "Not Available"
            ),

            "ceo": result.get(
                "companyOfficers",
                [{}]
            )[0].get(
                "name",
                "Not Available"
            ),

            "website": result.get(
                "website",
                "Not Available"
            ),

            "exchange": result.get(
                "exchange",
                "Not Available"
            ),

            "currency": result.get(
                "currency",
                "Not Available"
            ),

            "summary": result.get(
                "longBusinessSummary",
                ""
            )

        }

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )