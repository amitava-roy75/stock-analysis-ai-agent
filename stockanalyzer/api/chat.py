from fastapi import APIRouter

from models.chat_models import (
    ChatRequest,
    ChatResponse
)

from services.bedrock_service import (
    bedrock_service
)

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    answer = bedrock_service.chat(
        request.message
    )

    return ChatResponse(
        response=answer
    )