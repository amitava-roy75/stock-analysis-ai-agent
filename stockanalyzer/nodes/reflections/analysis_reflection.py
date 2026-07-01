import json
import re

from config.logging_config import logger
from prompts.reflection_prompt import REFLECTION_PROMPT
from services.bedrock_service import bedrock_service


class AnalysisReflection:
    """
    Generates the final institutional investment report.

    Responsibilities

    - Validate tool outputs
    - Invoke Bedrock
    - Parse JSON
    - Parse Markdown Report
    - Populate Graph State
    """

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Analysis Reflection Started")
        logger.info("========================================")

        tool_results = state.get("tool_results", [])

        #
        # Keep only successful tool results
        #

        successful_results = [

            item

            for item in tool_results

            if item.get("status") == "SUCCESS"

        ]

        if not successful_results:

            logger.warning("No successful tool results found.")

            state["summary"] = (
                "Unable to generate investment analysis because "
                "market data is unavailable."
            )

            state["recommendation"] = "NOT_AVAILABLE"

            state["confidence"] = "LOW"

            state["metrics"] = {}

            state["news"] = []

            state["final_answer"] = (
                "# Analysis Unavailable\n\n"
                "Insufficient market data was available."
            )

            return state

        #
        # Build prompt
        #

        prompt = f"""
{REFLECTION_PROMPT}

=========================================================

Tool Outputs

{json.dumps(successful_results, indent=2)}

=========================================================
"""

        try:

            logger.info("Calling Bedrock Reflection...")

            response = bedrock_service.chat(prompt)

            logger.info("========================================")
            logger.info("RAW REFLECTION RESPONSE")
            logger.info("========================================")
            logger.info(response)

            #
            # ------------------------------------------------------
            # Extract JSON
            # ------------------------------------------------------
            #

            json_data = {}

            report = ""

            json_match = re.search(
                r"<JSON>(.*?)</JSON>",
                response,
                flags=re.DOTALL | re.IGNORECASE,
            )

            if json_match:

                json_text = json_match.group(1).strip()

                try:

                    json_data = json.loads(json_text)

                except Exception:

                    logger.exception(
                        "Unable to parse JSON section."
                    )

            else:

                logger.warning(
                    "JSON block not found."
                )

            #
            # ------------------------------------------------------
            # Extract REPORT
            # ------------------------------------------------------
            #

            report_match = re.search(
                r"<REPORT>(.*?)</REPORT>",
                response,
                flags=re.DOTALL | re.IGNORECASE,
            )

            if report_match:

                report = report_match.group(1).strip()

            else:

                logger.warning(
                    "REPORT block not found."
                )

                #
                # Fallback
                #

                report = response

            #
            # ------------------------------------------------------
            # Populate State
            # ------------------------------------------------------
            #

            state["summary"] = json_data.get(
                "summary",
                ""
            )

            state["recommendation"] = json_data.get(
                "recommendation",
                "NOT_AVAILABLE"
            )

            state["confidence"] = json_data.get(
                "confidence",
                "LOW"
            )

            state["metrics"] = json_data.get(
                "metrics",
                {}
            )

            state["news"] = json_data.get(
                "news",
                []
            )

            state["final_answer"] = report

            logger.info("Analysis Reflection Completed.")

            return state

        except Exception as ex:

            logger.exception(ex)

            state["summary"] = (
                "Unable to generate investment report."
            )

            state["recommendation"] = "NOT_AVAILABLE"

            state["confidence"] = "LOW"

            state["metrics"] = {}

            state["news"] = []

            state["final_answer"] = (
                "# Analysis Failed\n\n"
                "An unexpected error occurred."
            )

            return state