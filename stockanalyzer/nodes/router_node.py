import asyncio
from typing import Any

from config.logging_config import logger
from tools.registry import registry


class RouterNode:

    async def __call__(self, state: dict) -> dict:

        logger.info("========== Router Node ==========")

        plan = state.get("plan", {})
        tasks = plan.get("tasks", [])

        if not tasks:
            logger.warning("No tasks found.")
            state["tool_results"] = []
            return state

        async def execute_task(task):

            tool_name = task["tool"]
            input_data = task["input"]

            logger.info(f"Executing {tool_name}")

            tool = registry.get(tool_name)

            if tool is None:
                return {
                    "tool": tool_name,
                    "status": "FAILED",
                    "message": "Unknown Tool"
                }

            try:

                result = await tool.execute(input_data)

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

        results = await asyncio.gather(
            *[execute_task(task) for task in tasks]
        )

        state["tool_results"] = results

        logger.info("Router Node Completed")

        return state