# ADR-005

## Context
ROADMAP v0.4 calls for ChromaDB + RAG. `TECH_STACK.md` names ChromaDB as the project's vector DB. There was no embedding or vector-search capability yet, and `/chat` had no way to ground responses in external documents.

## Decision
Add a RAG pipeline behind the same interface/provider/service shape as the rest of the app:
- `app/interfaces/embedding_provider.py` (`EmbeddingProvider`) and `app/interfaces/vector_store.py` (`VectorStore`) Protocols.
- `OllamaEmbeddingProvider` (`app/providers/`) implements `EmbeddingProvider` via Ollama's `/api/embed`, using the `nomic-embed-text` model (the only embedding model available locally; pulled via `ollama pull nomic-embed-text`).
- `ChromaVectorStore` (`app/rag/chroma_vector_store.py`) implements `VectorStore` against a Chroma `Collection`. `app/rag/chroma_client.py` creates the `HttpClient` and resolves a single `"documents"` collection.
- `RagService` (`app/services/rag_service.py`) orchestrates `ingest(text, metadata) -> id` and `retrieve(query, top_k) -> list[str]`.
- New endpoints `POST /documents` (ingest) and `POST /rag/query` (retrieve, for inspecting search results independently of chat).
- `/chat` integrates RAG as opt-in: `ChatRequest.use_rag: bool = False`. `ChatService.ask()` takes an optional `rag_service` and, when `use_rag=True`, retrieves chunks and passes them to `PromptBuilder.build()` as additional context. Default behavior (`use_rag=False`) is unchanged from v0.3.

Supporting decisions:
- **Chroma deployment**: dockerized server (`docker/docker-compose.yml`, `chromadb/chroma` image, port 8000), matching the Postgres pattern, over an embedded/in-process client. Chosen over embedded mode for parity with how Postgres is already run locally.
- **Client package**: `chromadb-client` (the thin HTTP-only client) instead of the full `chromadb` package, since the server runs separately in Docker and we don't need Chroma's bundled embedding models, ONNX runtime, or Kubernetes client. This keeps the dependency footprint small.
- **Embeddings via Ollama, not Chroma's built-in embedding function**: keeps embeddings on the same local LLM runtime as chat generation, consistent with the project's local-first goal, and avoids pulling in `onnxruntime`/`sentence-transformers`.
- **Single global `"documents"` collection**: no per-session or per-namespace separation yet; RAG documents are independent of conversation memory. Revisit if multi-tenant/document-scoping needs emerge.

Explicitly deferred (to avoid overengineering for an MVP):
- **Chunking strategy** — `ingest()` stores whatever text it's given as one chunk; splitting long documents is left for when real documents need it.
- **Re-ranking / hybrid search** — plain vector similarity via Chroma's default distance function is enough for now.

## Consequences
- New dependency: `chromadb-client`.
- New local infra: `chroma` service in `docker/docker-compose.yml` (port 8000); running the app or its RAG tests now also requires `docker compose -f docker/docker-compose.yml up -d`.
- New config: `CHROMA_HOST`, `CHROMA_PORT`, `EMBEDDING_MODEL` (`app/core/config.py`, `.env.example`).
- `ChatService.ask()` gained a `use_rag` parameter and an optional `rag_service` constructor argument; existing callers/tests that don't pass `use_rag` are unaffected (defaults to `False`).
- Unlike `ConversationMemory` (which swaps to a temporary SQLite file in tests), `chromadb-client`'s `HttpClient` has no embedded/local mode, so `tests/rag/test_chroma_vector_store.py` requires a real Chroma server reachable at `localhost:8000` (each test uses a uniquely named, self-deleting collection to avoid cross-test pollution). `RagService` and `ChatService` tests use fakes and need no infra.
