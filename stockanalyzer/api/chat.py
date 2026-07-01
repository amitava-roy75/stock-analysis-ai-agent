from fastapi import APIRouter, HTTPException

from models.chat_models import ChatRequest, ChatResponse

from services.bedrock_service import bedrock_service

from guardrails.guard_service import guard_service

from config.logging_config import logger


router = APIRouter(
    prefix="",
    tags=["Chat"]
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    try:

        logger.info("=========================================")
        logger.info("Chat Request")
        logger.info("Message : %s", request.message)
        logger.info("=========================================")

        #
        # Guard Rail
        #

        guard_service.validate(request.message)

        answer = bedrock_service.chat(
            request.message
        )

        return ChatResponse(
            response=answer
        )

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )