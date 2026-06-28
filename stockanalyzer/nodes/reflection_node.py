import json
import re

from config.logging_config import logger
from prompts.reflection_prompt import REFLECTION_PROMPT
from services.bedrock_service import bedrock_service


class ReflectionNode:
    """
    Reflection Node

    Generates the final stock analysis report using
    the outputs from all executed tools.

    It also extracts structured information that
    the frontend can consume directly.
    """

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Reflection Node Started")
        logger.info("========================================")

        tool_results = state.get("tool_results", [])

        prompt = f"""
{REFLECTION_PROMPT}

Below are the tool results.

{json.dumps(tool_results, indent=2, default=str)}

============================================================

VERY IMPORTANT

Return TWO sections.

SECTION 1

Return ONLY valid JSON enclosed between

<JSON>

...

</JSON>

JSON Schema

{{
    "summary": "",
    "recommendation": "BUY",
    "confidence": "HIGH",

    "metrics": {{
        "price": "",
        "marketCap": "",
        "pe": "",
        "roe": "",
        "dividendYield": ""
    }},

    "news": [
        {{
            "title": "",
            "summary": "",
            "publisher": "",
            "published": "",
            "sentiment": ""
        }}
    ]
}}

SECTION 2

Return the complete markdown report enclosed between

<REPORT>

...

</REPORT>

Do not return anything outside these two sections.

"""

        try:

            answer = bedrock_service.chat(prompt)

            logger.info("LLM Response Received")

            state["raw_answer"] = answer

            try:

                json_match = re.search(
                    r"<JSON>(.*?)</JSON>",
                    answer,
                    re.DOTALL,
                )

                report_match = re.search(
                    r"<REPORT>(.*?)</REPORT>",
                    answer,
                    re.DOTALL,
                )

                if json_match:

                    structured = json.loads(
                        json_match.group(1).strip()
                    )

                else:

                    structured = {}

                state["summary"] = structured.get(
                    "summary",
                    ""
                )

                state["recommendation"] = structured.get(
                    "recommendation",
                    "HOLD"
                )

                state["confidence"] = structured.get(
                    "confidence",
                    "LOW"
                )

                state["metrics"] = structured.get(
                    "metrics",
                    {}
                )

                state["news"] = structured.get(
                    "news",
                    []
                )

                if report_match:

                    state["final_answer"] = (
                        report_match.group(1).strip()
                    )

                else:

                    state["final_answer"] = answer

            except Exception as parse_error:

                logger.warning(
                    "Unable to parse structured response."
                )

                logger.exception(parse_error)

                state["summary"] = ""

                state["recommendation"] = "HOLD"

                state["confidence"] = "LOW"

                state["metrics"] = {}

                state["news"] = []

                state["final_answer"] = answer

            logger.info("Reflection Node Completed")

            return state

        except Exception as ex:

            logger.exception(ex)

            state["summary"] = ""

            state["recommendation"] = "HOLD"

            state["confidence"] = "LOW"

            state["metrics"] = {}

            state["news"] = []

            state["final_answer"] = str(ex)

            return state