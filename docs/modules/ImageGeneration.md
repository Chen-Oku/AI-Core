# Image Generation Module

## Purpose
Generate images from a text prompt via a local Stable Diffusion backend.

## Responsibilities
- Generate an image for a text prompt (`ImageProvider` interface, `Automatic1111ImageProvider` implementation).
- Orchestrate generation (`ImageService`).
- Expose generation over HTTP as `POST /images/generate`.

## Dependencies
- `app/interfaces/image_provider.py` — `Protocol` that `ImageService` depends on.
- `httpx` — calls the AUTOMATIC1111 WebUI's REST API (`POST /sdapi/v1/txt2img`); no official Python client package exists.
- A running AUTOMATIC1111 Stable Diffusion WebUI instance with `--api` enabled, reachable at `AUTOMATIC1111_BASE_URL` (not dockerized — run separately, like Ollama, since it needs GPU access).
- `app/core/config.py` — supplies `AUTOMATIC1111_BASE_URL`.
- Wired via `app/dependencies/image.py` (`get_image_provider`, `get_image_service`).

## Tests
- `backend/tests/services/test_image_service.py` — fake provider, no infra required.
- No direct test for `Automatic1111ImageProvider` against a live server, consistent with `OllamaProvider`/`OllamaEmbeddingProvider`.
