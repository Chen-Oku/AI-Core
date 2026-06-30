# Auth Module

## Purpose
Identify which tenant (consumer app) is calling AI Core, via a per-tenant API key, so other modules can scope data by tenant. Not user authentication — this is backend-to-backend auth between AI Core and the apps that consume it.

## Responsibilities
- Store API keys, hashed, mapped to a tenant name (`ApiKey` model, `app/auth/models.py`).
- Look up the tenant for a given key hash (`ApiKeyRepository` interface, `SqlAlchemyApiKeyRepository` implementation).
- Hash incoming raw keys and authenticate them (`AuthService.authenticate`).
- Resolve the calling tenant for every request and reject missing/invalid keys with `401` (`get_current_tenant` FastAPI dependency).

## Dependencies
- `app/interfaces/api_key_repository.py` — `ApiKeyRepository` Protocol that `AuthService` depends on.
- `app/core/db_base.py` — shared SQLAlchemy `Base`, also used by `app/memory/models.py`, so `api_keys` and `messages` live in the same schema, managed together by Alembic (ADR-010).
- Wired via `app/dependencies/auth.py` (`get_api_key_repository`, `get_auth_service`, `get_current_tenant`); `get_current_tenant` is a dependency on every router (`chat_router`, `agent_router`, `rag_router`, `image_router`).
- `app/dependencies/agent.py` also depends on `get_current_tenant` directly, to construct a tenant-scoped `RagSearchTool` per request (FastAPI caches the dependency result per request, so it isn't re-evaluated).

## Provisioning
No API endpoint creates keys (there's no authenticated way to call one before a key exists, and `Users`/`Organizations` aren't built yet). Run migrations first, then use the CLI script:

```bash
alembic upgrade head
python scripts/create_api_key.py <tenant-name>
```

Prints the raw key once; only its SHA-256 hash is stored. Callers send it as `X-API-Key: <key>` on every request.

## Tests
- `backend/tests/services/test_auth_service.py` — fakes, no infra required.
- `backend/tests/auth/test_sqlalchemy_api_key_repository.py` — SQLite, no Postgres required (same pattern as the memory module's tests).

See ADR-009.
