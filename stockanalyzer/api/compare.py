from fastapi import APIRouter, HTTPException

from models.compare_request import CompareRequest

from services.comparison_service import comparison_service

from guardrails.guard_service import guard_service

from config.logging_config import logger


router = APIRouter(
    prefix="",
    tags=["Comparison"]
)


@router.post("/compare")
async def compare(request: CompareRequest):

    try:

        logger.info("=========================================")
        logger.info("Compare Request")
        logger.info("Symbols : %s", request.symbols)
        logger.info("=========================================")

        #
        # Guard Rail
        #

        guard_service.validate(
            ",".join(request.symbols)
        )

        result = await comparison_service.compare(
            request.symbols
        )

        logger.info(
            "Comparison completed successfully."
        )

        return result

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )