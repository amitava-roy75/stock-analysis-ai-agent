from fastapi import HTTPException

from config.logging_config import logger

from guardrails.input_guard import input_guard


class GuardService:

    """
    Central Guard Service

    Every API should call this before executing
    any business logic.
    """

    def validate(self, query: str):

        result = input_guard.validate(query)

        if result.allowed:

            return

        logger.warning(
            "Request Blocked. Category=%s Reason=%s",
            result.category,
            result.reason
        )

        #
        # Never expose internal policy details
        #

        raise HTTPException(

            status_code=400,

            detail={

                "status": "BLOCKED",

                "message": (
                    "Your request violates the platform's "
                    "safety policy."
                ),

                "category": result.category

            }

        )


guard_service = GuardService()