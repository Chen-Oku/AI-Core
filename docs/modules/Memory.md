# Memory Module

## Purpose
Persist conversation history per session so chats survive a server restart.

## Responsibilities
- Resolve/generate a `session_id` for a request (`SessionManager`).
- Store and retrieve messages for a session (`ConversationMemory` interface, `SqlAlchemyConversationMemory` implementation).
- Own the SQLAlchemy schema/engine/session setup (`models.py`, `db.py`).

## Dependencies
- `app/interfaces/memory.py` — `ConversationMemory` Protocol that `ChatService` depends on.
- `sqlalchemy` + `psycopg[binary]` — ORM and PostgreSQL driver; the same implementation also works against SQLite (used by tests) by swapping the connection URL.
- `app/core/config.py` (`pydantic-settings`) — supplies `DATABASE_URL`.
- Wired via `app/dependencies/memory.py` (`get_db`, `get_session_manager`); `get_db` yields one `Session` per request.
- Local PostgreSQL for development: `docker/docker-compose.yml`.

## Tests
- `backend/tests/memory/test_sqlalchemy_conversation_memory.py`
- `backend/tests/memory/test_session_manager.py`
