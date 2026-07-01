from config.logging_config import logger

from prompts.compare_reflection_prompt import (
    COMPARE_REFLECTION_PROMPT,
)

from services.bedrock_service import bedrock_service


class ComparisonService:

    async def compare(self, tool_results: list):

        logger.info("========================================")
        logger.info("Comparison Service Started")
        logger.info("========================================")

        if not tool_results:

            return {

                "summary": "",

                "report": "",

                "stocks": []

            }

        #
        # ---------------------------------------------------------
        # Find CompareTool output
        # ---------------------------------------------------------
        #

        compare_data = None

        for item in tool_results:

            if (

                    item.get("tool") == "CompareTool"

                    and item.get("status") == "SUCCESS"

            ):

                compare_data = item.get("result")

                break

        if compare_data is None:

            logger.warning(
                "CompareTool output not found."
            )

            return {

                "summary": "",

                "report": "",

                "stocks": []

            }

        stocks = compare_data.get(
            "stocks",
            []
        )

        #
        # ---------------------------------------------------------
        # Generate comparison report using Bedrock
        # ---------------------------------------------------------
        #

        prompt = f"""
{COMPARE_REFLECTION_PROMPT}

=========================================================

Comparison Data

{stocks}

=========================================================

Generate

1. Executive Summary

2. Side-by-side comparison

3. Financial comparison

4. Strengths

5. Weaknesses

6. Investment Recommendation

Return markdown only.
"""

        logger.info("Generating comparison report...")

        report = bedrock_service.chat(prompt)

        #
        # ---------------------------------------------------------
        # Generate Summary
        # ---------------------------------------------------------
        #

        summary = ""

        for line in report.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            summary = line

            break

        return {

            "summary": summary,

            "report": report,

            "stocks": stocks

        }


comparison_service = ComparisonService()