from fastapi import APIRouter
from fastapi import HTTPException

from config.logging_config import logger
from graph.stock_graph import graph
from guardrails.guard_service import guard_service

router = APIRouter(
    prefix="",
    tags=["Stock Analysis"]
)


@router.get("/analyze")
async def analyze(query: str):

    try:

        logger.info("========================================")
        logger.info("Analyze Request")
        logger.info("Query : %s", query)
        logger.info("========================================")

        #
        # Input Guard
        #

        guard_service.validate(query)

        #
        # Initial Graph State
        #

        state = {

            "query": query,

            "intent": "",

            "company": "",

            "symbol": "",

            "plan": {},

            "tool_results": [],

            "messages": [],

            "summary": "",

            "recommendation": "",

            "confidence": "",

            "metrics": {},

            "news": [],

            "knowledge": "",

            "comparison": {},

            "final_answer": ""

        }

        result = await graph.ainvoke(state)

        intent = result.get(
            "intent",
            ""
        ).upper()

        #
        # ------------------------------------
        # KNOWLEDGE
        # ------------------------------------
        #

        if intent == "KNOWLEDGE":

            return {

                "query": query,

                "intent": intent,

                "summary": result.get(
                    "summary",
                    ""
                ),

                "report": result.get(
                    "final_answer",
                    ""
                )

            }

        #
        # ------------------------------------
        # COMPARE
        # ------------------------------------
        #

        if intent == "COMPARE":

            return {

                "query": query,

                "intent": intent,

                "summary": result.get(
                    "summary",
                    ""
                ),

                "report": result.get(
                    "final_answer",
                    ""
                )

            }

        #
        # ------------------------------------
        # ANALYZE
        # ------------------------------------
        #

        return {

            "query": query,

            "intent": intent,

            "company": result.get(
                "company",
                ""
            ),

            "symbol": result.get(
                "symbol",
                ""
            ),

            "summary": result.get(
                "summary",
                ""
            ),

            "recommendation": result.get(
                "recommendation",
                ""
            ),

            "confidence": result.get(
                "confidence",
                ""
            ),

            "metrics": result.get(
                "metrics",
                {}
            ),

            "news": result.get(
                "news",
                []
            ),

            "report": result.get(
                "final_answer",
                ""
            )

        }

    except HTTPException:
        raise

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )