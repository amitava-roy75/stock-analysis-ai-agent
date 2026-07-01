from config.logging_config import logger


class AnalysisNode:
    """
    Executes all tool results generated
    by RouterNode.

    No reflection happens here.
    """

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Analysis Node")
        logger.info("========================================")

        logger.info(
            "Tool Results : %d",
            len(state.get("tool_results", []))
        )

        return state