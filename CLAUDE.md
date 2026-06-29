# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role & Workflow (required)

Role: Senior Software Engineer.

Before writing code:
1. Explain the implementation plan.
2. List affected files.
3. Wait for approval before making architectural changes (new layers, new dependencies, new patterns).
4. Implement only the approved scope.
5. Suggest tests for the change.
6. Update `docs/CHANGELOG.md` and `docs/TODO.md`.

Architectural rules (enforced by review, not tooling):
- Business logic lives only in `services/`. Routers stay thin (parse request, call service, shape response).
- Use dependency injection — wire collaborators via `app/dependencies/*` and FastAPI's `Depends`, never instantiate providers/services directly inside routers.
- Code depends on interfaces (`app/interfaces/*`, `typing.Protocol`), not concrete implementations.
- Ask before introducing new architecture or libraries.
- Document architectural decisions as an ADR in `docs/adr/` (use `docs/templates/ADR_Template.md`).

## Project

AI Core is an early-stage, local-first, provider-agnostic AI platform meant to back web apps, game tooling, automation, and assistants (see `docs/PROJECT.md`). Only the chat path exists today; memory persistence, RAG, PostgreSQL, and agents are roadmap items (`docs/ROADMAP.md`, `docs/TODO.md`), not yet implemented. `frontend/`, `tests/` (root), `scripts/`, and `docker/` are currently empty placeholder directories — don't assume tooling exists there.

## Commands

All backend work happens inside `backend/`, which has its own `.venv`.

```bash
# from backend/, with the venv active
uvicorn app.main:app --reload
```

- `backend/requirements.txt` is currently empty — it has not been kept in sync with what's installed in `.venv`. If you add a dependency, `pip install` it into `backend/.venv` and also add it to `backend/requirements.txt`.
- Installed today (from `.venv`): `fastapi`, `uvicorn`, `pydantic`, `ollama`, `httpx`.
- No tests exist yet (`backend/tests/` is empty). Test runner is `pytest` per `docs/TECH_STACK.md`; there is no configured test command until tests are added.
- There is no lint/format tooling configured yet.

## Architecture

Layering (`docs/ARCHITECTURE.md`):

```
Client -> FastAPI -> Routers -> Services -> Interfaces -> Providers -> Models
```

- `app/api/` — FastAPI routers. Thin: validate via Pydantic schema, call a service, return a response schema. See [chat_router.py](backend/app/api/chat_router.py).
- `app/services/` — orchestration / business logic, e.g. [chat_service.py](backend/app/services/chat_service.py) coordinates a provider, a prompt builder, and conversation memory.
- `app/interfaces/` — `Protocol` definitions that services/routers depend on instead of concrete classes, e.g. `AIProvider` in [provider.py](backend/app/interfaces/provider.py).
- `app/providers/` — concrete `AIProvider` implementations (currently [ollama_provider.py](backend/app/providers/ollama_provider.py), hardcoded to model `qwen3:latest`). ADR-002 anticipates OpenAI/Claude/Gemini providers behind the same interface.
- `app/builders/` — construct prompts/context from conversation state, e.g. [prompt_builder.py](backend/app/builders/prompt_builder.py).
- `app/memory/` — conversation storage, e.g. [conversation_memory.py](backend/app/memory/conversation_memory.py) (currently an in-process list, no persistence/session scoping yet).
- `app/dependencies/` — FastAPI DI wiring (`get_provider`, `get_memory`, `get_chat_service`). This is where concrete implementations get bound to interfaces — new providers/services should be wired here, not constructed ad hoc in routers.
- `app/schemas/` — Pydantic request/response models for the API boundary.

When adding a new capability (e.g. a new provider, a new module), follow the existing module shape: interface in `interfaces/`, implementation in its own package, wiring in `dependencies/`, and a doc in `docs/modules/` (use `docs/templates/Module_Template.md`).

## Documentation map

- `docs/PROJECT.md`, `docs/ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/TECH_STACK.md`, `docs/PRINCIPLES.md` — read these first for intent and direction.
- `docs/adr/` — architectural decision records (DI, provider architecture, ...).
- `docs/modules/` — one doc per module (Chat, Memory, Providers).
- `docs/CONTRIBUTING.md` / `docs/guides/DevelopmentWorkflow.md` — feature flow: Design -> ADR (if needed) -> Implement -> Test -> Document -> Changelog.
- `docs/CHANGELOG.md`, `docs/TODO.md` — update these as part of any feature/fix, per the workflow above.
