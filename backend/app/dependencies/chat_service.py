from fastapi import Depends

from app.builders.prompt_builder import PromptBuilder
from app.dependencies.memory import get_session_manager
from app.dependencies.provider import get_provider
from app.services.chat_service import ChatService


def get_chat_service(

    provider = Depends(get_provider),

    session_manager = Depends(get_session_manager)

):

    prompt_builder = PromptBuilder()

    return ChatService(

        provider=provider,

        prompt_builder=prompt_builder,

        session_manager=session_manager

    )