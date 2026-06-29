from fastapi import Depends

from app.dependencies.memory import get_session_manager
from app.dependencies.provider import get_provider
from app.dependencies.rag import get_rag_service
from app.memory.session_manager import SessionManager
from app.providers.ollama_provider import OllamaProvider
from app.services.agent_service import AgentService
from app.services.rag_service import RagService
from app.tools.current_datetime_tool import CurrentDateTimeTool
from app.tools.rag_search_tool import RagSearchTool


def get_agent_service(
    provider: OllamaProvider = Depends(get_provider),
    rag_service: RagService = Depends(get_rag_service),
    session_manager: SessionManager = Depends(get_session_manager),
) -> AgentService:

    tools = [RagSearchTool(rag_service), CurrentDateTimeTool()]

    return AgentService(provider=provider, tools=tools, session_manager=session_manager)
