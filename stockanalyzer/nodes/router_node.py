import asyncio

from config.logging_config import logger
from tools.registry import registry
from nodes.knowledge_node import KnowledgeNode


class RouterNode:
    """
    Router Node

    Responsibilities

    1. Route KNOWLEDGE requests directly
    2. Execute tools for ANALYZE / COMPARE
    3. Store tool results
    """

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Router Node Started")
        logger.info("========================================")

        intent = state.get("intent", "").upper()

        #
        # ------------------------------------------
        # KNOWLEDGE
        # ------------------------------------------
        #

        if intent == "KNOWLEDGE":

            logger.info("Routing to Knowledge Node")

            node = KnowledgeNode()

            return await node(state)

        #
        # ------------------------------------------
        # ANALYZE / COMPARE
        # ------------------------------------------
        #

        plan = state.get("plan", {})

        tasks = plan.get("tasks", [])

        if not tasks:

            logger.warning("No tasks available.")

            state["tool_results"] = []

            return state

        async def execute_task(task):

            tool_name = task.get("tool")

            tool_input = task.get("input")

            logger.info(
                "Executing Tool : %s",
                tool_name
            )

            tool = registry.get(tool_name)

            if tool is None:

                logger.error(
                    "Unknown Tool : %s",
                    tool_name
                )

                return {

                    "tool": tool_name,

                    "status": "FAILED",

                    "message": "Unknown Tool"

                }

            try:

                result = await tool.execute(tool_input)

                return {

                    "tool": tool_name,

                    "status": "SUCCESS",

                    "result": result

                }

            except Exception as ex:

                logger.exception(ex)

                return {

                    "tool": tool_name,

                    "status": "FAILED",

                    "message": str(ex)

                }

        logger.info(
            "Executing %d tool(s)...",
            len(tasks)
        )

        results = await asyncio.gather(

            *[execute_task(task) for task in tasks]

        )

        state["tool_results"] = results

        logger.info("Router Node Completed")

        return state