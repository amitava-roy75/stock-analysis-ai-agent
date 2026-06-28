from fastapi import APIRouter, HTTPException

from models.analysis_response import AnalysisResponse
from config.logging_config import logger
from graph.stock_graph import graph

router = APIRouter(
    prefix="",
    tags=["Stock Analysis"]
)

@router.get(
    "/analyze",
    response_model=AnalysisResponse
)

async def analyze(query: str):
    """
    Execute the complete LangGraph workflow.

    Workflow

        Planner
            ↓
        Router
            ↓
        Reflection

    Returns

        {
            summary,
            recommendation,
            confidence,
            metrics,
            news,
            report
        }
    """

    try:

        logger.info("=========================================")
        logger.info("Analyze Request")
        logger.info("Query : %s", query)
        logger.info("=========================================")

        state = {

            "query": query,

            "intent": "",

            "company": "",

            "symbol": "",

            "plan": {},

            "tool_results": [],

            "messages": [],

            "summary": "",

            "recommendation": "HOLD",

            "confidence": "LOW",

            "metrics": {},

            "news": [],

            "final_answer": ""

        }

        #
        # IMPORTANT
        #
        # Since PlannerNode, RouterNode and ReflectionNode
        # are async, always use ainvoke()
        #

        result = await graph.ainvoke(state)

        logger.info("Workflow completed successfully")

        response = {

            "query": query,

            "intent": result.get(
                "intent",
                ""
            ),

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
                "HOLD"
            ),

            "confidence": result.get(
                "confidence",
                "LOW"
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

        logger.info("Returning structured response")

        return response

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )