from fastapi import APIRouter, Depends

from app.dependencies.chat_service import get_chat_service
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):

    response, session_id = chat_service.ask(request.message, request.session_id, request.use_rag)

    return ChatResponse(
        response=response,
        session_id=session_id
    )