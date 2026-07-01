import json
import re

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

    Responsibilities

    1. Detect Intent
    2. Build Execution Plan
    3. Validate Planner Output
    """

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Planner Node Started")
        logger.info("========================================")

        query = state.get("query", "").strip()
        lower_query = query.lower()

        #
        # ----------------------------------------------------------
        # KNOWLEDGE INTENT
        # ----------------------------------------------------------
        #

        knowledge_keywords = [

            "what is",
            "what are",
            "how",
            "why",
            "explain",
            "define",
            "meaning",
            "benefits",
            "types",
            "difference between mutual fund",
            "mutual fund",
            "stock market",
            "stock exchange",
            "etf",
            "sip",
            "nav",
            "dividend",
            "bond",
            "ipo"

        ]

        if any(keyword in lower_query for keyword in knowledge_keywords):

            logger.info("Intent detected : KNOWLEDGE")

            state["intent"] = "KNOWLEDGE"

            state["plan"] = {

                "intent": "KNOWLEDGE",

                "company": "",

                "symbol": "",

                "tasks": []

            }

            return state

        #
        # ----------------------------------------------------------
        # COMPARE INTENT
        # ----------------------------------------------------------
        #

        compare_match = re.search(

            r"compare\s+(.+?)\s+(?:vs|versus|and)\s+(.+)",

            lower_query,

            flags=re.IGNORECASE

        )

        if compare_match:

            stock1 = compare_match.group(1).strip().upper()
            stock2 = compare_match.group(2).strip().upper()

            logger.info(
                "Intent detected : COMPARE (%s vs %s)",
                stock1,
                stock2
            )

            state["intent"] = "COMPARE"

            state["plan"] = {

                "intent": "COMPARE",

                "company": "",

                "symbol": "",

                "tasks": [

                    {

                        "tool": "CompareTool",

                        "input": f"{stock1},{stock2}"

                    }

                ]

            }

            return state

        #
        # ----------------------------------------------------------
        # ANALYZE INTENT
        # ----------------------------------------------------------
        #

        logger.info("Invoking Bedrock Planner...")

        prompt = f"""
{PLANNER_PROMPT}

User Query

{query}
"""

        try:

            response = bedrock_service.chat(prompt)

            logger.info("Planner Response")

            logger.info(response)

            response = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            plan = json.loads(response)

            valid_tasks = []

            for task in plan.get("tasks", []):

                tool = task.get("tool")

                if tool in SUPPORTED_TOOLS:

                    valid_tasks.append(task)

                else:

                    logger.warning(
                        "Ignoring unsupported tool : %s",
                        tool
                    )

            plan["tasks"] = valid_tasks

            state["intent"] = plan.get(
                "intent",
                "ANALYZE"
            )

            state["company"] = plan.get(
                "company",
                ""
            )

            state["symbol"] = plan.get(
                "symbol",
                ""
            )

            state["plan"] = plan

            logger.info("Planner Completed Successfully")

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