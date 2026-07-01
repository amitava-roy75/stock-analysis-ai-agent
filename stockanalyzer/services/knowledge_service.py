from services.bedrock_service import bedrock_service
from prompts.knowledge_prompt import KNOWLEDGE_PROMPT

from config.logging_config import logger


class KnowledgeService:

    def ask(self, question: str) -> dict:
        """
        Generate an educational / financial knowledge response.

        This service is intentionally lightweight.

        Workflow

            Question
                ↓
            Knowledge Prompt
                ↓
            Amazon Bedrock
                ↓
            Markdown Response

        Returns a graph-compatible dictionary.
        """

        logger.info("=========================================")
        logger.info("Knowledge Service")
        logger.info("Question : %s", question)
        logger.info("=========================================")

        prompt = f"""
{KNOWLEDGE_PROMPT}

=========================================================

User Question

{question}

=========================================================

Generate a complete educational answer.

Return markdown only.
"""

        logger.info("Invoking Amazon Bedrock...")

        response = bedrock_service.chat(prompt)

        logger.info("Knowledge response generated successfully.")

        return {

            #
            # Used by Graph
            #
            "intent": "KNOWLEDGE",

            #
            # Reflection node can use this later
            #
            "knowledge": response,

            #
            # Keep Graph State compatible
            #
            "summary": "",

            "recommendation": "",

            "confidence": "",

            "metrics": {},

            "news": [],

            "tool_results": [],

            "messages": [

                {
                    "role": "assistant",
                    "content": response
                }

            ],

            #
            # Final markdown answer
            #
            "final_answer": response

        }


knowledge_service = KnowledgeService()