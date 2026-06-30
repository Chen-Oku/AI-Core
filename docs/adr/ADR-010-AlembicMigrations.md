# ADR-010

## Context
Schema changes (`Message`/`ApiKey` models) were applied via `Base.metadata.create_all()`, which only creates tables that don't yet exist — it never alters an existing one. ADR-009 hit this directly: a local Postgres DB with an old `messages` table (no `tenant` column) silently kept the stale schema until manually dropped and recreated. `docs/TODO.md` had tracked Alembic as deferred since ADR-004; two consecutive schema changes (ADR-008's chunk metadata didn't touch the schema, but ADR-009's tenant columns did, twice over) made the gap actively painful rather than theoretical.

## Decision
Adopt Alembic for schema management, scoped to `backend/`:
- `alembic.ini` / `alembic/env.py` / `alembic/versions/` (standard `alembic init` layout). `env.py` sets `target_metadata = Base.metadata` (`app/core/db_base.py`) and pulls the connection string from `app.core.config.settings.database_url` instead of a static `alembic.ini` entry, so there's one source of truth for `DATABASE_URL`.
- `app/core/db_models.py` — imports every ORM model (`Message`, `ApiKey`) purely for the side effect of registering them with `Base.metadata`. `env.py` imports it so `--autogenerate` sees the full schema. (This module already existed from the ADR-009 fix; it's now also alembic's registration point, not just init_db()'s.)
- One migration, `alembic/versions/1af1ac37aa0c_initial_schema.py`, generated via `alembic revision --autogenerate` against an empty database and hand-adjusted to use `sa.func.now()` instead of the SQLite-specific `CURRENT_TIMESTAMP` literal autogenerate produced (so the same migration is correct on both SQLite and Postgres). Verified by running `alembic upgrade head` against a throwaway empty Postgres database and inspecting the resulting schema.
- **`app/dependencies/memory.py` and `scripts/create_api_key.py` no longer call `init_db()`.** Schema creation/upgrades are now an explicit operational step (`alembic upgrade head`), not a side effect of importing the FastAPI app or running a script. The existing local Postgres database (already at the correct schema, manually fixed during ADR-009 validation) was marked current with `alembic stamp head` rather than re-run.
- **`app/memory/db.py`'s `init_db()` is unchanged and still used by tests** (`tests/memory/`, `tests/auth/`), which point SQLAlchemy at a fresh temporary SQLite file per test and call `create_all()` directly. Tests don't care about migration history, only the final schema shape, and running real migrations per test would slow the suite for no benefit.

Supporting decisions:
- **Autogenerate against an empty DB, not the live one**: diffing against the user's already-correct local Postgres would have produced an empty (no-op) migration, useless for a fresh environment (CI, a new developer, a different deployment) that needs to create the schema from nothing.
- **One squashed initial migration instead of one per historical ADR**: there's no real deployment running the pre-ADR-009 schema that needs an incremental migration path — recreating that history would document churn nobody needs to replay.

## Consequences
- New dependency: `alembic` (`backend/requirements.txt`).
- Breaking change to the startup sequence: starting the app or running `scripts/create_api_key.py` against a database that hasn't run `alembic upgrade head` now fails with "relation does not exist" instead of silently creating the schema. `CLAUDE.md`'s Commands section documents the required step.
- Future schema changes go through `alembic revision --autogenerate -m "..."` (reviewed before committing, autogenerate isn't always exactly right) + `alembic upgrade head`, not by just changing a model and restarting the app.
- No test changes — the test suite's SQLite fixtures are intentionally untouched by this ADR.
