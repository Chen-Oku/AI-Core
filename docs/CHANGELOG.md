# Changelog

## Unreleased
- Add per-session, SQLite-persisted conversation memory (`SqliteConversationMemory`, `SessionManager`) behind a `ConversationMemory` interface; `/chat` now accepts/returns `session_id` (ADR-003)
- Remove in-process `ConversationMemory` (superseded by the persisted version)

## v0.1.0
- Implement `/chat` endpoint: router, `ChatService`, `OllamaProvider`, `PromptBuilder`, in-process `ConversationMemory`, DI wiring
- Remove undocumented empty stubs (`app/core`, `app/database`, `app/models`) and stray root `requirements.txt`
- Add root `.gitignore`
- Initial project
