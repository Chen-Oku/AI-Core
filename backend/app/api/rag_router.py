from fastapi import APIRouter, Depends

from app.dependencies.rag import get_rag_service
from app.schemas.rag_schema import IngestRequest, IngestResponse, RetrieveRequest, RetrieveResponse
from app.services.rag_service import RagService

router = APIRouter()


@router.post("/documents", response_model=IngestResponse)
def ingest(
    request: IngestRequest,
    rag_service: RagService = Depends(get_rag_service)
):

    document_id = rag_service.ingest(request.text, request.metadata)

    return IngestResponse(id=document_id)


@router.post("/rag/query", response_model=RetrieveResponse)
def query(
    request: RetrieveRequest,
    rag_service: RagService = Depends(get_rag_service)
):

    chunks = rag_service.retrieve(request.query, request.top_k)

    return RetrieveResponse(chunks=chunks)
