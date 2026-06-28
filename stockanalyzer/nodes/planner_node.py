import json

from config.logging_config import logger
from prompts.planner_prompt import PLANNER_PROMPT
from services.bedrock_service import bedrock_service


SUPPORTED_TOOLS = {
    "PriceTool",
    "NewsTool",
    "FundamentalTool",
    "CompanyProfileTool",
    "FinancialStatementTool",
    "CompareTool",
}


class PlannerNode:
    """
    Planner Node

    Converts a natural language query into
    a structured execution plan.
    """

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Planner Node Started")
        logger.info("========================================")

        query = state.get("query", "")

        prompt = f"""
{PLANNER_PROMPT}

User Query:

{query}
"""

        try:

            response = bedrock_service.chat(prompt)

            logger.info("Raw Planner Response:")
            logger.info(response)

            #
            # Remove markdown fences
            #

            response = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            plan = json.loads(response)

            #
            # Validate tools
            #

            valid_tasks = []

            for task in plan.get("tasks", []):

                tool = task.get("tool")

                if tool in SUPPORTED_TOOLS:
                    valid_tasks.append(task)

                else:

                    logger.warning(
                        f"Unsupported tool ignored : {tool}"
                    )

            plan["tasks"] = valid_tasks

            state["intent"] = plan.get("intent", "")

            state["company"] = plan.get("company", "")

            state["symbol"] = plan.get("symbol", "")

            state["plan"] = plan

            logger.info("Planner Node Completed")

            return state

        except Exception as ex:

            logger.exception(ex)

            state["intent"] = "ERROR"

            state["plan"] = {

                "intent": "ERROR",

                "company": "",

                "symbol": "",

                "tasks": []

            }

            return state