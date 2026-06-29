from fastapi import Depends

from app.builders.prompt_builder import PromptBuilder
from app.dependencies.provider import get_provider
from app.providers.ollama_provider import OllamaProvider
from app.services.chat_service import ChatService
from fastapi import Depends
from app.dependencies.memory import get_memory


def get_chat_service(

    provider = Depends(get_provider),

    memory = Depends(get_memory)

):

    prompt_builder = PromptBuilder()

    return ChatService(

        provider=provider,

        prompt_builder=prompt_builder,

        memory=memory

    )