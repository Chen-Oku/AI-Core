# ADR-009

## Context
Every endpoint (`/chat`, `/agent`, `/documents`, `/rag/query`, `/images/generate`) was open with no authentication, and RAG (`"documents"` Chroma collection) and conversation memory (`messages` table) had no concept of which caller a piece of data belonged to — ADR-005 explicitly deferred this ("Revisit if multi-tenant/document-scoping needs emerge"). With a second consumer (Career Intelligence Platform) about to integrate against AI Core instead of a stand-in API, both gaps needed closing: unauthenticated access to a backend meant to be called by multiple independent apps, and no isolation between those apps' data once more than one exists.

Authentication and multi-tenant isolation are treated as one slice because isolation needs an identity to scope by, and that identity is exactly what authentication produces — building one without the other would mean inventing a throwaway tenant concept now and rewiring it later.

## Decision
Add API Key authentication, and thread the resulting tenant identity through RAG and conversation memory as a scoping key:

- **`app/auth/`** (mirrors the `app/memory/` module shape): `models.py` defines `ApiKey` (`key_hash`, `tenant`, `is_active`, `created_at`); `sqlalchemy_api_key_repository.py` implements `find_active_tenant_by_hash(key_hash) -> str | None` against it.
- **`app/interfaces/api_key_repository.py`**: `ApiKeyRepository` Protocol that `AuthService` depends on.
- **`app/services/auth_service.py`**: `AuthService.authenticate(raw_key) -> str` hashes the raw key (SHA-256) and looks up the tenant via the repository; raises `AuthenticationError` if missing/inactive. Only the hash is ever persisted.
- **`app/dependencies/auth.py`**: `get_current_tenant`, a FastAPI dependency reading the `X-API-Key` header, raising `401` on a missing/invalid key. Added to every router (`chat_router`, `agent_router`, `rag_router`, `image_router`) — `image_router` ignores the resolved value (`_tenant`) since image generation isn't scoped, but still requires a valid key.
- **Provisioning**: `backend/scripts/create_api_key.py`, a standalone CLI script that generates a random key (`secrets.token_urlsafe(32)`), stores only its hash, and prints the raw key once. No admin/create-key endpoint exists — there's no way to authenticate a request to create the first key, and `Users`/`Organizations` aren't built yet (out of scope per the charter's "do not implement unless requested"). A local CLI script sidesteps that bootstrap problem and matches the project's local-first operating model.
- **Tenant scoping in RAG**: `RagService.ingest(text, tenant, metadata)` tags every chunk's metadata with `tenant` (alongside the `document_id`/`chunk_index` from ADR-008); `RagService.retrieve(query, tenant, top_k)` passes `where={"tenant": tenant}` to the vector store. `VectorStore.query()` gained a `where: dict | None = None` parameter; `ChromaVectorStore.query()` forwards it to Chroma's own `where` filtering.
- **Tenant scoping in memory**: `Message` gained a `tenant` column. `SessionManager.get_or_create(session_id, tenant)` and `SqlAlchemyConversationMemory(db, session_id, tenant)` now require it and filter/write by the `(session_id, tenant)` pair.
- **Agent tool wiring**: `RagSearchTool` now takes `tenant` at construction (`app/dependencies/agent.py` builds it per-request from `get_current_tenant`, the same resolved value the router uses — FastAPI caches a dependency's result for the lifetime of one request, so `get_current_tenant` only actually runs once per call even though both `agent_router` and `get_agent_service` depend on it).
- **Shared `Base`**: moved out of `app/memory/models.py` into `app/core/db_base.py` so `app/auth/models.py` and `app/memory/models.py` register tables against the same SQLAlchemy metadata. `app/dependencies/memory.py` imports `app.auth.models` before calling `init_db()` so `api_keys` gets created too — a SQLAlchemy declarative quirk (`create_all()` only sees models that have been imported somewhere), not a new pattern.

Supporting decisions:
- **Isolation by construction, not by rejection**: a tenant passing another tenant's `session_id` simply sees an empty conversation (no rows match `(session_id, tenant)`), rather than the service explicitly detecting and rejecting cross-tenant access. Fewer failure modes, same isolation guarantee.
- **API key as a flat string over JWT/OAuth**: this is backend-to-backend auth between trusted local services, not end-user auth — consistent with the project's local-first scope and avoids pulling in a token/identity-provider library prematurely.
- **`tenant` is a required parameter, no default, on `RagService.ingest`/`retrieve`**: forces every call site to consciously supply scoping rather than silently defaulting to an unscoped (cross-tenant) query.

Explicitly deferred:
- `Users`/`Organizations`/multiple keys per tenant/key rotation/revocation endpoint — only single-key-per-tenant creation exists today (rerunning the script for the same tenant just adds another active key, which already works for rotation by creation, but there's no way to deactivate/revoke an old one without a direct DB update).
- Rate limiting / usage metering per tenant.
- Alembic migrations: `Message`/`ApiKey` schema changes rely on `Base.metadata.create_all()`, which only creates missing tables and does not alter existing ones. A pre-existing local Postgres database needs its `messages`/`api_keys` tables dropped (or the DB recreated) to pick up the new `tenant`/`api_keys` schema — acceptable pre-production, tracked as the existing Alembic TODO item.

## Consequences
- Breaking change: every endpoint now requires a valid `X-API-Key` header (`401` otherwise). Any existing manual/Postman testing needs a key from `scripts/create_api_key.py` first.
- Breaking change to method signatures: `RagService.ingest`/`retrieve`, `ChatService.ask`, `AgentService.ask`, `SessionManager.get_or_create`, `SqlAlchemyConversationMemory.__init__`, `RagSearchTool.__init__`, and `VectorStore.query` all gained a required `tenant`/`where` parameter. All call sites and tests were updated.
- New tables: `api_keys` (via the shared `Base`/`init_db()` already used for `messages`).
- New tests: `backend/tests/services/test_auth_service.py` (fakes), `backend/tests/auth/test_sqlalchemy_api_key_repository.py` (SQLite, no Postgres needed, same pattern as the memory module's tests). Existing RAG/memory/chat/agent/tool tests updated for the new required parameters and gained tenant-isolation cases.
