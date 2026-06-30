from fastapi import Depends

from app.core.config import settings
from app.providers.ollama_embedding_provider import OllamaEmbeddingProvider
from app.rag.chroma_client import create_chroma_client, get_or_create_collection
from app.rag.chroma_vector_store import ChromaVectorStore
from app.services.rag_service import RagService

chroma_client = create_chroma_client(settings.chroma_host, settings.chroma_port)
collection = get_or_create_collection(chroma_client, "documents")


def get_embedding_provider() -> OllamaEmbeddingProvider:

    return OllamaEmbeddingProvider(settings.embedding_model)


def get_vector_store() -> ChromaVectorStore:

    return ChromaVectorStore(collection)


def get_rag_service(
    embedding_provider: OllamaEmbeddingProvider = Depends(get_embedding_provider),
    vector_store: ChromaVectorStore = Depends(get_vector_store),
) -> RagService:

    return RagService(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
        chunk_size=settings.rag_chunk_size,
        chunk_overlap=settings.rag_chunk_overlap,
    )
