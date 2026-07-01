from config.logging_config import logger


class KnowledgeReflection:
    """
    Knowledge Reflection

    Validates and finalizes educational responses.
    No LLM call is made here—the KnowledgeService has
    already generated the content.
    """

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Knowledge Reflection Started")
        logger.info("========================================")

        report = state.get("final_answer", "")

        #
        # Fallback to knowledge field if needed
        #

        if not report:
            report = state.get("knowledge", "")

        #
        # Nothing generated
        #

        if not report:

            logger.warning("Knowledge response is empty.")

            state["summary"] = (
                "Unable to generate educational content."
            )

            state["final_answer"] = (
                "Sorry, I could not generate the requested educational content."
            )

            return state

        #
        # Generate summary from first paragraph
        #

        summary = ""

        lines = report.splitlines()

        for line in lines:

            line = line.strip()

            #
            # Skip headings
            #

            if not line:
                continue

            if line.startswith("#"):
                continue

            summary = line

            break

        if not summary:

            summary = report[:250].strip()

        if len(summary) > 300:
            summary = summary[:300] + "..."

        state["summary"] = summary

        state["final_answer"] = report

        logger.info("Knowledge Reflection Completed")

        return state