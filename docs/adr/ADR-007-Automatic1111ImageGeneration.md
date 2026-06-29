# ADR-007

## Context
ROADMAP v1.0 and `docs/TODO.md` call for image generation. Ollama (the project's local LLM runtime) has no text-to-image capability, so a different local backend is needed. The project is local-first, so a commercial API (OpenAI Images, Stability AI) was rejected for this first slice in favor of a self-hosted option, matching how Ollama/Postgres/Chroma are all run locally.

## Decision
Add an image generation slice behind the same interface/provider/service/router shape as RAG:
- `app/interfaces/image_provider.py` (`ImageProvider`) Protocol: `generate(prompt: str) -> str`, returning a base64-encoded PNG.
- `Automatic1111ImageProvider` (`app/providers/automatic1111_provider.py`) implements `ImageProvider` against the AUTOMATIC1111 Stable Diffusion WebUI's REST API (`POST /sdapi/v1/txt2img`), called directly via `httpx` (already a dependency) since there's no official Python client package.
- `ImageService` (`app/services/image_service.py`) orchestrates `generate(prompt) -> str`.
- New endpoint `POST /images/generate`, returning `{"image_base64": ...}`.

Supporting decisions:
- **Backend choice**: AUTOMATIC1111 WebUI, the most common local Stable Diffusion REST API, over ComfyUI (graph/workflow-based, more complex integration for an MVP) and over commercial APIs (breaks local-first for this feature).
- **Response shape**: base64 string embedded in the JSON response, mirroring what AUTOMATIC1111 itself returns, rather than saving files to disk. Avoids a storage/retention concern for this first slice.
- **Deployment**: not added to `docker/docker-compose.yml`. Unlike Postgres/Chroma, AUTOMATIC1111 needs GPU access and is not a simple stock image; it's run separately by the user (with `--api` enabled), the same way Ollama itself runs separately. Configured via `AUTOMATIC1111_BASE_URL` (`app/core/config.py`, `.env.example`).
- **Agent tool integration deferred**: only a dedicated endpoint for now, no `ImageGenerationTool` wired into `AgentService`. Follows the RAG precedent (`POST /documents`/`POST /rag/query` shipped before `RagSearchTool`).

Explicitly deferred (to avoid overengineering for an MVP):
- Generation parameters beyond `prompt` (negative prompt, size, steps, sampler, seed) — AUTOMATIC1111's own defaults are used.
- Saving generated images or tracking generation history.

## Consequences
- New config: `AUTOMATIC1111_BASE_URL` (`app/core/config.py`, `.env.example`/`.env`).
- New local infra requirement: a running AUTOMATIC1111 WebUI instance with `--api` enabled, reachable at `AUTOMATIC1111_BASE_URL`. Not provided by `docker/docker-compose.yml`.
- No changes to existing modules (`ChatService`, `RagService`, `AgentService` are untouched).
- No direct test for `Automatic1111ImageProvider` against a live server — consistent with `OllamaProvider`/`OllamaEmbeddingProvider`, which also aren't tested directly against their live backend. `ImageService` is tested with a fake provider (`backend/tests/services/test_image_service.py`).
- Adding generation parameters or an agent tool later only requires extending `ImageProvider`/`ImageService` and, for the tool, following the `RagSearchTool` pattern — no other wiring changes.
