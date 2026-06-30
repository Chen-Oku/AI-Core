from fastapi import APIRouter, Depends

from app.dependencies.agent import get_agent_service
from app.dependencies.auth import get_current_tenant
from app.schemas.agent_schema import AgentRequest, AgentResponse
from app.services.agent_service import AgentService

router = APIRouter()


@router.post("/agent", response_model=AgentResponse)
def agent(
    request: AgentRequest,
    tenant: str = Depends(get_current_tenant),
    agent_service: AgentService = Depends(get_agent_service)
):

    response, session_id = agent_service.ask(request.message, request.session_id, tenant)

    return AgentResponse(
        response=response,
        session_id=session_id
    )
