from pydantic import BaseModel


class IngestRequest(BaseModel):
    text: str
    metadata: dict | None = None


class IngestResponse(BaseModel):
    id: str


class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 3


class RetrieveResponse(BaseModel):
    chunks: list[str]
