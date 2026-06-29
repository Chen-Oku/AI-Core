# Memory Module

## Purpose
Persist conversation history per session so chats survive a server restart.

## Responsibilities
- Resolve/generate a `session_id` for a request (`SessionManager`).
- Store and retrieve messages for a session (`ConversationMemory` interface, `SqliteConversationMemory` implementation).
- Own the SQLite schema/connection setup (`database.py`).

## Dependencies
- `app/interfaces/memory.py` — `ConversationMemory` Protocol that `ChatService` depends on.
- stdlib `sqlite3` — no external dependency.
- Wired via `app/dependencies/memory.py` (`get_session_manager`).

## Tests
- `backend/tests/memory/test_sqlite_conversation_memory.py`
- `backend/tests/memory/test_session_manager.py`
