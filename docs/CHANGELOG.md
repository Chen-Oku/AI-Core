# Changelog

## Unreleased
- Add Alembic schema migrations: `backend/alembic/` (`env.py` targets the shared `Base.metadata` and `settings.database_url`), one squashed initial migration creating `messages`/`api_keys`. The app and `scripts/create_api_key.py` no longer call `init_db()`/`create_all()` at startup — run `alembic upgrade head` first. Tests are unaffected (still use `create_all()` against temporary SQLite). New `app/core/db_models.py` registers all ORM models for `--autogenerate` (ADR-010)
- Add API Key authentication and multi-tenant isolation: `app/auth/` module (`ApiKey` model, `SqlAlchemyApiKeyRepository`), `AuthService.authenticate()`, `get_current_tenant` FastAPI dependency requiring `X-API-Key` on every endpoint (`401` if missing/invalid), `scripts/create_api_key.py` CLI for provisioning. `RagService.ingest`/`retrieve`, `ChatService.ask`, `AgentService.ask`, `SessionManager.get_or_create`, `SqlAlchemyConversationMemory`, `RagSearchTool`, and `VectorStore.query` all now require a `tenant`/`where` parameter to scope RAG documents and conversation memory per tenant. Moved the shared SQLAlchemy `Base` to `app/core/db_base.py` (ADR-009)
- Add chunking to the RAG ingest path: `app/rag/chunker.py:split_text` (fixed-size, overlapping); `RagService.ingest()` now splits text into chunks, embeds/stores each separately tagged with `document_id`/`chunk_index` in metadata, and returns `(document_id, chunk_count)`. `POST /documents` response changed from `{id}` to `{document_id, chunk_count}`. New `RAG_CHUNK_SIZE`/`RAG_CHUNK_OVERLAP` config (ADR-008)
- Add Image Generation: `ImageProvider` interface, `Automatic1111ImageProvider` (calls a local AUTOMATIC1111 Stable Diffusion WebUI's `txt2img` API via `httpx`), `ImageService`; new `POST /images/generate` endpoint returning a base64-encoded PNG (ADR-007). Add `AUTOMATIC1111_BASE_URL` to config/`.env.example`
- Add Agents + Tool Calling: `Tool`/`ToolCallingProvider` interfaces, `OllamaProvider.chat()`, `AgentService` (ReAct-style tool loop with a `MAX_ITERATIONS` safety bound), `rag_search`/`current_datetime` tools, new `POST /agent` endpoint (ADR-006)
- Add RAG pipeline: `EmbeddingProvider`/`VectorStore` interfaces, `OllamaEmbeddingProvider`, `ChromaVectorStore`, `RagService` (`ingest`/`retrieve`); new `POST /documents` and `POST /rag/query` endpoints (ADR-005)
- Integrate RAG into `/chat` as opt-in: `ChatRequest.use_rag` (default `False`); `ChatService.ask()` retrieves context via `RagService` and `PromptBuilder` injects it into the prompt when enabled
- Add `chroma` service to `docker/docker-compose.yml` (Chroma server, port 8000); add `CHROMA_HOST`/`CHROMA_PORT`/`EMBEDDING_MODEL` to config/`.env.example`
- Migrate conversation persistence from raw `sqlite3` to SQLAlchemy + PostgreSQL (`SqlAlchemyConversationMemory`, `app/memory/models.py`, `app/memory/db.py`) behind the same `ConversationMemory` interface; no change to `ChatService`/`/chat` (ADR-004)
- Add `app/core/config.py` (`pydantic-settings`) for `DATABASE_URL`; add `docker/docker-compose.yml` for local PostgreSQL
- Remove `SqliteConversationMemory`/`database.py` (superseded)

## v0.2.0
- Add per-session, SQLite-persisted conversation memory (`SqliteConversationMemory`, `SessionManager`) behind a `ConversationMemory` interface; `/chat` now accepts/returns `session_id` (ADR-003)
- Remove in-process `ConversationMemory` (superseded by the persisted version)

## v0.1.0
- Implement `/chat` endpoint: router, `ChatService`, `OllamaProvider`, `PromptBuilder`, in-process `ConversationMemory`, DI wiring
- Remove undocumented empty stubs (`app/core`, `app/database`, `app/models`) and stray root `requirements.txt`
- Add root `.gitignore`
- Initial project
