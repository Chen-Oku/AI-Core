# ADR-008

## Context
ADR-005 explicitly deferred chunking: `RagService.ingest()` stored whatever text it was given as a single chunk/embedding. This breaks down for real documents (e.g. a full CV or career profile) longer than an embedding model's effective context — the embedding dilutes across the whole text and retrieval quality drops. `docs/TODO.md` tracked this as a known gap.

## Decision
Add fixed-size character chunking with overlap to the ingest path, without introducing a new dependency or a new interface:
- `app/rag/chunker.py`: `split_text(text, chunk_size, chunk_overlap) -> list[str]`, a pure function. Returns `[text]` unchanged when it already fits in one chunk; otherwise slides a `chunk_size`-character window forward by `chunk_size - chunk_overlap` each step. Raises `ValueError` if `chunk_overlap >= chunk_size`.
- `RagService.ingest()` now splits the input text via `split_text`, embeds and stores each chunk separately, and tags every chunk's metadata with `document_id` (shared across all chunks of that ingest call) and `chunk_index`. Returns `(document_id, chunk_count)` instead of a bare id.
- `RagService` takes `chunk_size`/`chunk_overlap` as constructor parameters (defaults `500`/`50`), supplied in `app/dependencies/rag.py` from new `Settings.rag_chunk_size`/`rag_chunk_overlap` (`app/core/config.py`, `.env.example`: `RAG_CHUNK_SIZE`, `RAG_CHUNK_OVERLAP`).
- `IngestResponse` (`app/schemas/rag_schema.py`) changed from `{id}` to `{document_id, chunk_count}`, so callers can see how a document was split.

Supporting decisions:
- **Fixed-size character splitting over a library** (e.g. LangChain text splitters): keeps the dependency footprint small, consistent with the precedent set in ADR-005 (`chromadb-client` over full `chromadb`, Ollama embeddings over Chroma's bundled ones). A semantic/sentence-aware splitter is real future work but is overkill for the current single-collection MVP.
- **`document_id` + `chunk_index` in metadata, not a separate table**: keeps chunk provenance queryable via Chroma's existing `metadata`/`where` filtering without adding new infrastructure.
- **Single global `chunk_size`/`chunk_overlap` via settings, not per-request**: avoids expanding `IngestRequest` for a tuning knob that's an operational concern, not a per-call one. Revisit if different document types need different chunking strategies.

Explicitly still deferred:
- Semantic/sentence-aware chunking.
- Re-ranking across chunks of the same document at retrieval time (currently `retrieve()` returns raw top-k chunks, which may include multiple chunks from the same document or none from a more relevant one).

## Consequences
- Breaking change to `RagService.ingest()`'s return type (`str` -> `tuple[str, int]`) and to `POST /documents`'s response shape (`id` -> `document_id`/`chunk_count`). No other module called `ingest()` directly (`RagSearchTool` only calls `retrieve()`), so no other code changed.
- Every stored chunk now carries `document_id`/`chunk_index` in `metadata`, merged with any caller-supplied `metadata`. Callers using metadata key names `document_id`/`chunk_index` for their own purposes would collide — none do today.
- New config: `RAG_CHUNK_SIZE`, `RAG_CHUNK_OVERLAP` (`app/core/config.py`, `.env.example`).
- New tests: `backend/tests/rag/test_chunker.py` (pure function, no infra); `backend/tests/rag/test_rag_service.py` gained a multi-chunk case and the existing single-chunk case was updated for the new metadata/return shape.
