from pydantic import BaseModel


class AgentRequest(BaseModel):
    message: str
    session_id: str | None = None


class AgentResponse(BaseModel):
    response: str
    session_id: str
