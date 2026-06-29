# RAG Module

## Purpose
Ground chat responses in external documents via retrieval-augmented generation: store text as embeddings, and retrieve the most relevant chunks for a given query.

## Responsibilities
- Generate embeddings for text (`EmbeddingProvider` interface, `OllamaEmbeddingProvider` implementation).
- Store and search embeddings (`VectorStore` interface, `ChromaVectorStore` implementation).
- Orchestrate ingest/retrieve (`RagService`).
- Optionally augment `/chat` prompts with retrieved context when `use_rag=True`.

## Dependencies
- `app/interfaces/embedding_provider.py`, `app/interfaces/vector_store.py` — Protocols that `RagService` depends on.
- `ollama` — embedding generation via the `nomic-embed-text` model (`EMBEDDING_MODEL` setting); must be pulled locally with `ollama pull nomic-embed-text`.
- `chromadb-client` + a running Chroma server — vector storage/search; the same `"documents"` collection is used for all ingestion.
- `app/core/config.py` — supplies `CHROMA_HOST`, `CHROMA_PORT`, `EMBEDDING_MODEL`.
- Wired via `app/dependencies/rag.py` (`get_embedding_provider`, `get_vector_store`, `get_rag_service`).
- Local Chroma server for development: `docker/docker-compose.yml` (port 8000).
- `ChatService` depends on `RagService` (optional) to retrieve context when a `/chat` request sets `use_rag: true`.

## Tests
- `backend/tests/rag/test_rag_service.py` — fakes, no infra required.
- `backend/tests/rag/test_chroma_vector_store.py` — requires a real Chroma server at `localhost:8000`.
- `backend/tests/services/test_chat_service.py` — covers `use_rag` wiring with fakes.
