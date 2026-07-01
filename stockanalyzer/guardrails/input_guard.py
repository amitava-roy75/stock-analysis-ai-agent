import re

from config.logging_config import logger

from guardrails.guard_result import GuardResult
from guardrails.policies import BLOCKED_PATTERNS


class InputGuard:
    """
    Input Guard Rail

    Responsibilities

        • Validate user input

        • Detect prompt injection

        • Detect jailbreak attempts

        • Detect profanity / violence / hate

        • Return a GuardResult

    This guard is intentionally lightweight.

    Later it can be enhanced with:

        • Amazon Bedrock Guardrails

        • LLM-based safety validation

        • PII detection

        • Prompt attack detection

        • Toxicity classification
    """

    def validate(self, text: str) -> GuardResult:

        logger.info("========================================")
        logger.info("Input Guard Validation")
        logger.info("========================================")

        if not text:

            return GuardResult(
                allowed=False,
                reason="Empty request.",
                category="EMPTY"
            )

        query = text.lower()

        #
        # Scan all configured policies
        #

        for category, patterns in BLOCKED_PATTERNS.items():

            for pattern in patterns:

                if re.search(pattern, query):

                    logger.warning(
                        "Input blocked. Category=%s Pattern=%s",
                        category,
                        pattern
                    )

                    return GuardResult(
                        allowed=False,
                        reason=f"Blocked by security policy ({category}).",
                        category=category
                    )

        logger.info("Input Guard Passed.")

        return GuardResult(
            allowed=True
        )


input_guard = InputGuard()