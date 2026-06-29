# TODO

- Alembic migrations (once the schema needs to change)
- Chunking strategy for long documents ingested into RAG (currently stored as a single chunk)
- Image generation parameters beyond `prompt` (negative prompt, size, steps, sampler, seed)
- `ImageGenerationTool` to let the Agent generate images mid-conversation (deferred from ADR-007, same shape as `RagSearchTool`)
- Audio (STT/TTS)
