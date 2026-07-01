from config.logging_config import logger

from services.knowledge_service import knowledge_service


class KnowledgeNode:

    async def __call__(self, state: dict):

        logger.info("========================================")
        logger.info("Knowledge Node")
        logger.info("========================================")

        query = state.get(
            "query",
            ""
        )

        response = knowledge_service.ask(
            query
        )

        #
        # Merge response
        #

        state.update(response)

        logger.info(
            "Knowledge generated successfully."
        )

        return state