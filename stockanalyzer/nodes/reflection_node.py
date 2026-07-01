from config.logging_config import logger

from nodes.reflections.analysis_reflection import AnalysisReflection
from nodes.reflections.compare_reflection import CompareReflection
from nodes.reflections.knowledge_reflection import KnowledgeReflection


class ReflectionNode:
    """
    Reflection Router

    Routes the graph state to the appropriate
    reflection implementation based on intent.

        ANALYZE   -> AnalysisReflection

        COMPARE   -> CompareReflection

        KNOWLEDGE -> KnowledgeReflection
    """

    def __init__(self):

        self.analysis = AnalysisReflection()

        self.compare = CompareReflection()

        self.knowledge = KnowledgeReflection()

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Reflection Node Started")
        logger.info("========================================")

        intent = state.get(
            "intent",
            ""
        ).upper()

        logger.info("Intent : %s", intent)

        #
        # -------------------------------------------------------
        # KNOWLEDGE
        # -------------------------------------------------------
        #

        if intent == "KNOWLEDGE":

            logger.info(
                "Routing to Knowledge Reflection"
            )

            return await self.knowledge(state)

        #
        # -------------------------------------------------------
        # COMPARE
        # -------------------------------------------------------
        #

        if intent == "COMPARE":

            logger.info(
                "Routing to Compare Reflection"
            )

            return await self.compare(state)

        #
        # -------------------------------------------------------
        # ANALYZE
        # -------------------------------------------------------
        #

        logger.info(
            "Routing to Analysis Reflection"
        )

        return await self.analysis(state)