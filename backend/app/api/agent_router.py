from fastapi import APIRouter, Depends

from app.dependencies.agent import get_agent_service
from app.schemas.agent_schema import AgentRequest, AgentResponse
from app.services.agent_service import AgentService

router = APIRouter()


@router.post("/agent", response_model=AgentResponse)
def agent(
    request: AgentRequest,
    agent_service: AgentService = Depends(get_agent_service)
):

    response, session_id = agent_service.ask(request.message, request.session_id)

    return AgentResponse(
        response=response,
        session_id=session_id
    )
