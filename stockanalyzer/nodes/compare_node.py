from config.logging_config import logger

from services.comparison_service import comparison_service


class CompareNode:

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Compare Node")
        logger.info("========================================")

        results = state.get(
            "tool_results",
            []
        )

        response = await comparison_service.compare(results)

        state["summary"] = response.get(
            "summary",
            ""
        )

        state["final_answer"] = response.get(
            "report",
            ""
        )

        state["comparison"] = response

        return state