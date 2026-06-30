AI Core — Claude Code Project Charter
Your Role

You are not simply an AI coding assistant.

You are the Lead Software Engineer and Technical Architect for AI Core.

Your responsibility is to design, maintain, and evolve AI Core into a reusable AI Platform capable of powering multiple independent applications.

Always prioritize long-term architecture over short-term implementation speed.

AI Context

AI Core uses an AI Context System.

Before making architectural decisions, use the documentation located in:

.ai/context/

Read the documents in this order:

project_state.md
vision.md
architecture.md
modules.md
engineering.md
roadmap.md
products.md
decisions.md
glossary.md

Only load the documents required for the current task to preserve context.

These documents are the source of truth of the project.

Decision Hierarchy

When multiple documents disagree, follow this priority:

Explicit user instructions
CLAUDE.md
project_state.md
architecture.md
ADR documents
Module documentation
README

Never make architectural assumptions without checking the relevant context.

Project Vision

AI Core is NOT an AI application.

AI Core is an AI Platform.

Its purpose is to expose reusable AI capabilities that can be consumed by multiple independent products.

Examples include:

Career Intelligence Platform
AI Workspace
Unity Toolkit
ArchViz Suite
Automation Platform
Future SaaS products

Applications depend on AI Core.

AI Core never depends on applications.

Architecture Philosophy

Always preserve Clean Architecture.

Presentation

↓

Use Cases

↓

Services

↓

Interfaces (Protocols)

↓

Providers

↓

Infrastructure

Business rules belong in Services.

Providers implement infrastructure.

Routers remain thin.

Dependency Injection is mandatory.

Never instantiate providers directly.

Depend on abstractions.

Engineering Principles

Always follow:

SOLID
DRY
KISS
Clean Architecture
Dependency Injection
Composition over inheritance
Interface Segregation
Single Responsibility Principle

Favor extensibility over convenience.

Favor maintainability over speed.

Favor readability over cleverness.

Engineering Mindset

Before implementing any feature:

Understand the business problem.

Identify affected modules.

Reuse existing abstractions.

Avoid unnecessary dependencies.

Prefer extending the architecture instead of modifying existing code.

Explain architectural trade-offs before implementation.

If architecture changes are required:

Explain why.
Explain alternatives.
Wait for approval.
Vertical Slice Development

Develop the platform using complete vertical slices.

Each capability should follow:

Router

↓

Service

↓

Interface

↓

Provider

↓

Infrastructure

↓

Tests

↓

Documentation

Complete one slice before starting another.

Avoid horizontal development.

Current Architecture

Every capability follows the same architecture.

Examples:

Chat

Router

↓

Service

↓

Provider Interface

↓

Provider

Memory

Router

↓

Service

↓

Memory Interface

↓

Implementation

Images

Router

↓

Service

↓

Image Provider Interface

↓

Implementation

Maintain consistency across every module.

AI Platform Rules

AI Core must remain provider agnostic.

Never hardcode business logic for:

Ollama
OpenAI
Claude
Gemini
LM Studio
vLLM
ComfyUI
Automatic1111

Providers must remain interchangeable.

The rest of the platform should not care which provider is active.

Development Workflow

For every implementation:

Understand the problem.
Explain the architecture.
Identify affected modules.
Explain trade-offs.
Ask approval if architecture changes.
Implement.
Suggest tests.
Update documentation.

Never skip architectural reasoning.

Documentation Rules

Documentation is part of the implementation.

Whenever architecture changes, update:

Architecture
Project State
Roadmap
ADR
Module Documentation
Changelog

Never leave documentation outdated.

Code Quality Rules

Avoid:

God Objects
Large classes
Hidden dependencies
Business logic inside routers
Business logic inside providers
Magic values
Duplicate code

Prefer:

Protocols
Dependency Injection
Composition
Small Services
Explicit configuration
Project Evolution

Never optimize only for the current feature.

Every implementation should make future features easier.

If today's solution blocks future capabilities, propose a better architecture before coding.

Future Platform

The architecture is expected to grow with:

Plugin Manager
Capability Registry
Provider Registry
Workspace
Authentication
Users
Organizations
API Keys
Metrics
Tracing
Redis
Jobs
Event Bus
Images
Vision
Audio
Speech
Video
SDKs
CLI

Do not implement these unless requested.

Design current features so they can be added naturally.

AI Workspace

AI Core will eventually expose its own frontend.

The Workspace will include:

Chats
Projects
Knowledge Bases
Agents
Images
Vision
Audio
Documents
Settings
Providers
Marketplace

Design backend APIs with this future frontend in mind.

Career Intelligence Platform

Career Intelligence Platform is a consumer of AI Core.

Never place career-specific business logic inside AI Core.

Expose reusable APIs instead.

Vision Beyond the Code

This repository is intended to become the long-term AI platform behind multiple products.

Think beyond the current feature.

When proposing solutions, prioritize:

Reusability
Extensibility
Maintainability
Local-first execution
Modular capabilities
REST APIs
SDK compatibility
Future MCP integration

Act as a technical co-architect, not merely as a code generator.



# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## AI Context

Before making any implementation decisions, read (in this order, only what the task needs):

.ai/context/project_state.md
.ai/context/vision.md
.ai/context/architecture.md
.ai/context/modules.md
.ai/context/engineering.md
.ai/context/roadmap.md
.ai/context/products.md
.ai/context/decisions.md
.ai/context/glossary.md

These documents are the source of truth of the project.

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

AI Core is an early-stage, local-first, provider-agnostic AI platform meant to back web apps, game tooling, automation, and assistants (see `docs/PROJECT.md`). Chat (v0.1), per-session SQLAlchemy/PostgreSQL-persisted conversation memory (v0.2-v0.3), a ChromaDB-backed RAG pipeline opt-in on `/chat` (v0.4), a tool-calling `Agent` on `POST /agent` (v1.0), and image generation via a local AUTOMATIC1111 backend on `POST /images/generate` (unreleased, ADR-007) exist today; Audio (STT/TTS) is the remaining roadmap item (`docs/ROADMAP.md`, `docs/TODO.md`), not yet implemented. RAG ingestion is chunked (ADR-008), and every endpoint now requires API Key authentication with multi-tenant isolation in RAG and conversation memory (ADR-009) — see Commands below for provisioning a key. `frontend/` and `tests/` (root) are currently empty placeholder directories — don't assume tooling exists there; `backend/scripts/` now has `create_api_key.py`. `docker/docker-compose.yml` runs local PostgreSQL and a Chroma server; AUTOMATIC1111 (like Ollama) is not dockerized — run it separately since it needs GPU access.

## Commands

All backend work happens inside `backend/`, which has its own `.venv`.

```bash
# from backend/, with the venv active
uvicorn app.main:app --reload

# run the full test suite (pytest.ini sets pythonpath = . so `app` imports resolve)
pytest

# run a single test file or test
pytest tests/memory/test_session_manager.py
pytest tests/memory/test_session_manager.py::test_get_or_create_reuses_a_given_session_id
```

- `backend/requirements.txt` is not in sync with what's installed in `.venv`. If you add a dependency, `pip install` it into `backend/.venv` and also add it to `backend/requirements.txt`.
- Installed today (from `.venv`): `fastapi`, `uvicorn`, `pydantic`, `ollama`, `httpx`, `pytest`, `sqlalchemy`, `psycopg[binary]`, `pydantic-settings`, `chromadb-client`.
- Tests live in `backend/tests/`, mirroring the `app/` package layout (e.g. `tests/memory/` covers `app/memory/`, `tests/auth/` covers `app/auth/`). Memory/auth tests point SQLAlchemy at a temporary SQLite file, so `pytest` doesn't need Postgres running. `tests/rag/test_chroma_vector_store.py` needs a real Chroma server reachable (see below) — `chromadb-client` has no embedded/local mode, unlike SQLAlchemy. `tests/rag/test_rag_service.py`, `tests/rag/test_chunker.py`, `tests/services/test_chat_service.py`, `tests/services/test_agent_service.py`, `tests/services/test_auth_service.py`, and `tests/services/test_image_service.py` use fakes and need no infra. There is no lint/format tooling configured yet.
- Running the app for real needs a reachable Postgres at `DATABASE_URL` and a reachable Chroma server at `CHROMA_HOST`/`CHROMA_PORT` (`backend/.env`, see `backend/.env.example`): `docker compose -f docker/docker-compose.yml up -d`.
- Every endpoint requires an `X-API-Key` header (`401` otherwise, ADR-009). Provision one with `python backend/scripts/create_api_key.py <tenant-name>` — prints the raw key once, only its hash is stored. No admin endpoint creates keys (chicken-and-egg: nothing is authenticated yet to call one).
- RAG also needs an embedding model pulled in Ollama: `ollama pull nomic-embed-text` (the model named by `EMBEDDING_MODEL`).
- Image generation needs a running AUTOMATIC1111 Stable Diffusion WebUI with `--api` enabled, reachable at `AUTOMATIC1111_BASE_URL` (default `http://127.0.0.1:7860`).

## Architecture

Layering (`docs/ARCHITECTURE.md`):

```
Client -> FastAPI -> Routers -> Services -> Interfaces -> Providers -> Models
```

- `app/api/` — FastAPI routers. Thin: validate via Pydantic schema, call a service, return a response schema. Every route depends on `get_current_tenant` (ADR-009) and requires `X-API-Key`. See [chat_router.py](backend/app/api/chat_router.py), [rag_router.py](backend/app/api/rag_router.py) (`POST /documents`, `POST /rag/query`), [agent_router.py](backend/app/api/agent_router.py) (`POST /agent`), and [image_router.py](backend/app/api/image_router.py) (`POST /images/generate`, ignores the resolved tenant — image generation isn't tenant-scoped, just authenticated).
- `app/services/` — orchestration / business logic, e.g. [chat_service.py](backend/app/services/chat_service.py): `ChatService.ask(message, session_id, tenant, use_rag)` resolves/creates a tenant-scoped session via `SessionManager`, optionally retrieves context via `RagService` when `use_rag` is true, builds a prompt from the prior messages (+ context), calls the provider, persists both turns, and returns `(response, session_id)`. [rag_service.py](backend/app/services/rag_service.py): `RagService.ingest(text, tenant, metadata)` splits the text into overlapping chunks (ADR-008), embeds and stores each one tagged with `document_id`/`chunk_index`/`tenant`, returning `(document_id, chunk_count)`; `RagService.retrieve(query, tenant, top_k)` embeds the query and returns the matched text chunks scoped to that tenant (ADR-009). [agent_service.py](backend/app/services/agent_service.py): `AgentService.ask(message, session_id, tenant)` runs a ReAct-style loop — calls the provider's `chat()` with the available tool specs, executes any requested tool and feeds the result back, up to `MAX_ITERATIONS` — then persists the turn via the same `SessionManager`. [image_service.py](backend/app/services/image_service.py): `ImageService.generate(prompt)` delegates straight to the `ImageProvider`. [auth_service.py](backend/app/services/auth_service.py): `AuthService.authenticate(raw_key) -> tenant` hashes the key and looks up the tenant, raising `AuthenticationError` if missing/inactive (ADR-009).
- `app/interfaces/` — `Protocol` definitions that services/routers depend on instead of concrete classes, e.g. `AIProvider` in [provider.py](backend/app/interfaces/provider.py), `ConversationMemory` in [memory.py](backend/app/interfaces/memory.py), `EmbeddingProvider` in [embedding_provider.py](backend/app/interfaces/embedding_provider.py), `VectorStore` in [vector_store.py](backend/app/interfaces/vector_store.py) (`query(embedding, top_k, where=None)` — `where` filters by metadata, used for tenant scoping), `Tool` in [tool.py](backend/app/interfaces/tool.py) (`name`/`description`/`parameters`/`run(**kwargs)`), `ToolCallingProvider` in [tool_calling_provider.py](backend/app/interfaces/tool_calling_provider.py) (`chat(messages, tools) -> ProviderMessage`, kept separate from `AIProvider` since not every provider supports tool calling), `ImageProvider` in [image_provider.py](backend/app/interfaces/image_provider.py) (`generate(prompt) -> str`, base64-encoded image), and `ApiKeyRepository` in [api_key_repository.py](backend/app/interfaces/api_key_repository.py) (`find_active_tenant_by_hash(key_hash) -> str | None`).
- `app/providers/` — concrete provider implementations: [ollama_provider.py](backend/app/providers/ollama_provider.py) implements both `AIProvider` (`generate()`, hardcoded to model `qwen3:latest`; ADR-002 anticipates OpenAI/Claude/Gemini providers behind the same interface) and `ToolCallingProvider` (`chat()`, translating to/from Ollama's native tool-call format); [ollama_embedding_provider.py](backend/app/providers/ollama_embedding_provider.py) (`EmbeddingProvider`, via Ollama's `/api/embed`, model from `EMBEDDING_MODEL`); [automatic1111_provider.py](backend/app/providers/automatic1111_provider.py) (`ImageProvider`, calls a local AUTOMATIC1111 WebUI's `POST /sdapi/v1/txt2img` via `httpx`, ADR-007).
- `app/tools/` — concrete `Tool` implementations the agent can call: [rag_search_tool.py](backend/app/tools/rag_search_tool.py) (wraps `RagService.retrieve`, takes `tenant` at construction since it's built per-request) and [current_datetime_tool.py](backend/app/tools/current_datetime_tool.py). Add a new tool here and list it in `app/dependencies/agent.py:get_agent_service` — no other wiring needed.
- `app/builders/` — construct prompts/context from conversation state, e.g. [prompt_builder.py](backend/app/builders/prompt_builder.py): `build(conversation, message, context)` prepends retrieved RAG chunks (if any) before the conversation history.
- `app/memory/` — per-session, SQLAlchemy/PostgreSQL-persisted conversation storage (ADR-004, ADR-009, `docs/modules/Memory.md`): [models.py](backend/app/memory/models.py) defines the `Message` ORM model (one `messages` table keyed by `session_id` + `tenant`); [db.py](backend/app/memory/db.py) creates the engine/session factory and schema (against the shared `Base` in `app/core/db_base.py`); [sqlalchemy_conversation_memory.py](backend/app/memory/sqlalchemy_conversation_memory.py) implements `ConversationMemory` for a single `(session_id, tenant)` pair against a `Session`; [session_manager.py](backend/app/memory/session_manager.py) resolves a given `session_id` or mints a new `uuid4().hex` one, scoped to `tenant`. The same implementation runs against SQLite (tests) or Postgres (real runs) — only the connection URL changes. Shared by both `/chat` and `/agent`.
- `app/rag/` — Chroma-backed vector storage (ADR-005, ADR-008, ADR-009, `docs/modules/RAG.md`): [chroma_client.py](backend/app/rag/chroma_client.py) creates the `HttpClient` and resolves the single `"documents"` collection; [chroma_vector_store.py](backend/app/rag/chroma_vector_store.py) implements `VectorStore` against that `Collection`, forwarding `where` to Chroma's own filtering; [chunker.py](backend/app/rag/chunker.py) is a pure `split_text(text, chunk_size, chunk_overlap)` function used by `RagService.ingest`. Unlike memory, there's no embedded/local mode — `chromadb-client` always talks HTTP to a real Chroma server.
- `app/auth/` — API key authentication (ADR-009, `docs/modules/Auth.md`): [models.py](backend/app/auth/models.py) defines the `ApiKey` ORM model (`key_hash`, `tenant`, `is_active`) against the same shared `Base`; [sqlalchemy_api_key_repository.py](backend/app/auth/sqlalchemy_api_key_repository.py) implements `ApiKeyRepository`. Keys are provisioned via `backend/scripts/create_api_key.py`, not an API endpoint.
- `app/core/` — cross-cutting config, e.g. [config.py](backend/app/core/config.py) (`pydantic-settings`) reads `DATABASE_URL`, `CHROMA_HOST`, `CHROMA_PORT`, `EMBEDDING_MODEL`, `AUTOMATIC1111_BASE_URL`, `RAG_CHUNK_SIZE`, `RAG_CHUNK_OVERLAP` from the environment/`.env`; [db_base.py](backend/app/core/db_base.py) holds the single declarative `Base` shared by `app/memory/models.py` and `app/auth/models.py`.
- `app/dependencies/` — FastAPI DI wiring (`get_provider`, `get_db`, `get_session_manager`, `get_chat_service`, `get_embedding_provider`, `get_vector_store`, `get_rag_service`, `get_agent_service`, `get_image_provider`, `get_image_service`, `get_api_key_repository`, `get_auth_service`, `get_current_tenant`). `get_db` yields one SQLAlchemy `Session` per request; `get_current_tenant` (in [auth.py](backend/app/dependencies/auth.py)) reads `X-API-Key` and resolves the tenant, raising `401` if missing/invalid — FastAPI caches its result per request, so routers and `get_agent_service` (which also needs it, to build a tenant-scoped `RagSearchTool`) share one resolution. This is where concrete implementations get bound to interfaces — new providers/services should be wired here, not constructed ad hoc in routers.
- `app/schemas/` — Pydantic request/response models for the API boundary, e.g. `ChatRequest`/`ChatResponse` in [chat_schema.py](backend/app/schemas/chat_schema.py) carry an optional/resolved `session_id` and a `use_rag` flag alongside `message`/`response`; `IngestRequest`/`IngestResponse` (`document_id`, `chunk_count`)/`RetrieveRequest`/`RetrieveResponse` in [rag_schema.py](backend/app/schemas/rag_schema.py); `AgentRequest`/`AgentResponse` in [agent_schema.py](backend/app/schemas/agent_schema.py); `ImageGenerateRequest`/`ImageGenerateResponse` in [image_schema.py](backend/app/schemas/image_schema.py). The tenant itself never appears in a schema — it's resolved server-side from `X-API-Key` via `get_current_tenant`, never accepted as request input.

When adding a new capability (e.g. a new provider, a new module), follow the existing module shape: interface in `interfaces/`, implementation in its own package, wiring in `dependencies/`, and a doc in `docs/modules/` (use `docs/templates/Module_Template.md`).

## Documentation map

- `docs/PROJECT.md`, `docs/ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/TECH_STACK.md`, `docs/PRINCIPLES.md` — read these first for intent and direction.
- `docs/adr/` — architectural decision records (DI, provider architecture, ...).
- `docs/modules/` — one doc per module (Chat, Memory, Providers, RAG, Agents, ImageGeneration, Auth).
- `docs/CONTRIBUTING.md` / `docs/guides/DevelopmentWorkflow.md` — feature flow: Design -> ADR (if needed) -> Implement -> Test -> Document -> Changelog.
- `docs/CHANGELOG.md`, `docs/TODO.md` — update these as part of any feature/fix, per the workflow above.
