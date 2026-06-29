# Agents Module

## Purpose
Let the LLM decide, mid-conversation, to invoke a tool (e.g. search the knowledge base) and use the result to produce its final answer, instead of relying on a fixed, always-on pipeline.

## Responsibilities
- Define what a tool is and how to describe/run one (`Tool` interface).
- Translate between the provider-agnostic tool-calling shape and a specific provider's wire format (`ToolCallingProvider` interface, `OllamaProvider.chat()`).
- Run the call -> tool -> call loop until the model returns a final answer or a safety limit is hit (`AgentService`).
- Persist agent conversations the same way chat conversations are persisted.

## Dependencies
- `app/interfaces/tool.py` — `Tool` Protocol that `AgentService` depends on.
- `app/interfaces/tool_calling_provider.py` — `ToolCallingProvider` Protocol, `ProviderMessage`/`ToolCall` dataclasses.
- `app/providers/ollama_provider.py` — `OllamaProvider.chat()` implements `ToolCallingProvider` against Ollama's native tool calling (model `qwen3:latest`).
- `app/tools/rag_search_tool.py` (depends on `RagService`, ADR-005) and `app/tools/current_datetime_tool.py` — the two MVP tools.
- `app/memory/session_manager.py` — reused as-is for conversation persistence.
- Wired via `app/dependencies/agent.py` (`get_agent_service`).

## Tests
- `backend/tests/services/test_agent_service.py` — fakes for provider/tool/session manager, no infra required; covers the no-tool-call path, the tool-call-then-answer path, and the `MAX_ITERATIONS` safety bound.
- `backend/tests/tools/test_rag_search_tool.py`, `backend/tests/tools/test_current_datetime_tool.py`.
