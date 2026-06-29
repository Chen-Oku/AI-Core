from fastapi import Depends

from app.builders.prompt_builder import PromptBuilder
from app.dependencies.memory import get_session_manager
from app.dependencies.provider import get_provider
from app.dependencies.rag import get_rag_service
from app.services.chat_service import ChatService


def get_chat_service(

    provider = Depends(get_provider),

    session_manager = Depends(get_session_manager),

    rag_service = Depends(get_rag_service)

):

    prompt_builder = PromptBuilder()

    return ChatService(

        provider=provider,

        prompt_builder=prompt_builder,

        session_manager=session_manager,

        rag_service=rag_service

    )