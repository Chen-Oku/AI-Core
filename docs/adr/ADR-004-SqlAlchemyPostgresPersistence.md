# ADR-004

## Context
ADR-003 used raw `sqlite3` for v0.2 and explicitly deferred the move to SQLAlchemy/PostgreSQL to v0.3 (ROADMAP), behind the existing `ConversationMemory` interface. `TECH_STACK.md` names PostgreSQL as the project's database.

## Decision
Replace `SqliteConversationMemory`/`database.py` with a single `SqlAlchemyConversationMemory`, backed by a SQLAlchemy `Session` and a `Message` ORM model (`app/memory/models.py`). The same implementation works against either SQLite or PostgreSQL — only the connection URL changes — so it covers both local/test runs and the real Postgres target without two parallel implementations.

Supporting decisions made alongside this:
- **Config layer**: introduce `app/core/config.py` (`pydantic-settings`) to read `DATABASE_URL` from the environment/`.env`, replacing the previous hardcoded path. This is the first piece of an `app/core/` config module other parts of the app (RAG, providers) will likely reuse.
- **DB session per request**: `app/dependencies/memory.py` now exposes a `get_db` generator dependency (one `Session` per request, closed after) instead of opening a connection per method call.
- **Local Postgres via Docker**: `docker/docker-compose.yml` runs Postgres for local development, since `docker/` was an empty placeholder for exactly this.
- **Driver**: `psycopg` v3 (`psycopg[binary]`), a synchronous driver, matching the rest of the stack (FastAPI routes and the Ollama provider are sync).

Explicitly deferred (to avoid overengineering for a single-table schema):
- **Alembic migrations** — `Base.metadata.create_all` is enough while there's one table and no schema churn. Introduce Alembic when a real migration (schema change on existing data) is needed.
- **Async SQLAlchemy/asyncpg** — no async boundary exists elsewhere in the stack yet; introducing it only here would add complexity without a matching benefit.

## Consequences
- New dependencies: `sqlalchemy`, `psycopg[binary]`, `pydantic-settings`.
- `ChatService` and `/chat` are unaffected — `ConversationMemory` is unchanged.
- Running the app now requires a reachable database at `DATABASE_URL` (default points at the docker-compose Postgres); tests don't need Postgres since they point SQLAlchemy at a temporary SQLite file.
- Schema changes after this point require manual care (no migration tool yet) until Alembic is introduced.
