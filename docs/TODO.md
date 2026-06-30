# TODO

- Image generation parameters beyond `prompt` (negative prompt, size, steps, sampler, seed)
- `ImageGenerationTool` to let the Agent generate images mid-conversation (deferred from ADR-007, same shape as `RagSearchTool`)
- Audio (STT/TTS)
- Semantic/sentence-aware chunking and cross-chunk re-ranking at retrieval time (deferred from ADR-008)
- API key rotation/revocation (an endpoint or script to deactivate a key, list a tenant's keys) — only creation exists today (ADR-009)
- Rate limiting / usage metering per tenant (ADR-009)
