from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_tenant
from app.dependencies.rag import get_rag_service
from app.schemas.rag_schema import IngestRequest, IngestResponse, RetrieveRequest, RetrieveResponse
from app.services.rag_service import RagService

router = APIRouter()


@router.post("/documents", response_model=IngestResponse)
def ingest(
    request: IngestRequest,
    tenant: str = Depends(get_current_tenant),
    rag_service: RagService = Depends(get_rag_service)
):

    document_id, chunk_count = rag_service.ingest(request.text, tenant, request.metadata)

    return IngestResponse(document_id=document_id, chunk_count=chunk_count)


@router.post("/rag/query", response_model=RetrieveResponse)
def query(
    request: RetrieveRequest,
    tenant: str = Depends(get_current_tenant),
    rag_service: RagService = Depends(get_rag_service)
):

    chunks = rag_service.retrieve(request.query, tenant, request.top_k)

    return RetrieveResponse(chunks=chunks)
