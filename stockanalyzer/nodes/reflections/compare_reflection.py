from config.logging_config import logger

from services.comparison_service import comparison_service


class CompareReflection:
    """
    Compare Reflection

    Executes the ComparisonService to generate
    the comparison report and updates the graph state.
    """

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Compare Reflection Started")
        logger.info("========================================")

        #
        # Generate comparison report
        #

        comparison = await comparison_service.compare(
            state.get("tool_results", [])
        )

        state["comparison"] = comparison

        report = comparison.get("report", "")

        if not report:

            logger.warning(
                "Comparison report not available."
            )

            state["summary"] = (
                "Comparison could not be completed."
            )

            state["final_answer"] = (
                "Comparison report could not be generated."
            )

            return state

        #
        # Populate state
        #

        state["summary"] = comparison.get(
            "summary",
            ""
        )

        state["final_answer"] = report

        logger.info(
            "Compare Reflection Completed"
        )

        return state