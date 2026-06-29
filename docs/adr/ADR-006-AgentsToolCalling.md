# ADR-006

## Context
ROADMAP v1.0 calls for Agents + Tool Calling. The existing `AIProvider.generate(prompt: str) -> str` is single-turn and string-only: it can't express a list of available tools, a multi-message conversation, or a model's request to call one. Verified directly against Ollama that `qwen3:8b` supports native tool calling (`ollama.chat(..., tools=[...])` returns `message.tool_calls` with parsed name/arguments) and that a full round trip (call -> tool result fed back -> final answer) works.

## Decision
Add a `ToolCallingProvider` Protocol (`app/interfaces/tool_calling_provider.py`) separate from `AIProvider`, rather than extending `AIProvider` itself (Interface Segregation: not every provider will support tool calling, and `ChatService`/`/chat` don't need it). It returns a provider-agnostic `ProviderMessage(content, tool_calls: list[ToolCall])` so callers never see Ollama's native response shape. `OllamaProvider` implements both `AIProvider` (unchanged `generate()`) and `ToolCallingProvider` (new `chat()`), translating to/from Ollama's wire format internally.

`Tool` (`app/interfaces/tool.py`) is a Protocol with `name`, `description`, a JSON-schema `parameters` dict, and `run(**kwargs) -> str`. Two MVP implementations in `app/tools/`:
- `RagSearchTool` — wraps the existing `RagService.retrieve()` (ADR-005), letting the agent decide when retrieval is actually needed instead of always-on (`use_rag`).
- `CurrentDateTimeTool` — a trivial, dependency-free second tool, added to prove the tool registry handles more than one tool, not because it's a target use case.

`AgentService` (`app/services/agent_service.py`) runs a ReAct-style loop: send the conversation + tool specs to the provider; if it returns tool calls, run each tool and append the results as `{"role": "tool", ...}` messages, then ask again; repeat up to `MAX_ITERATIONS = 5` (a hardcoded safety bound — if the model keeps calling tools without converging, the loop stops and returns a fallback message instead of looping forever or against the model indefinitely).

New endpoint `POST /agent`, separate from `/chat` (different orchestration shape — multi-turn tool loop vs. single prompt build — not a flag on `ChatService`). Reuses the existing `SessionManager`/`ConversationMemory` so agent and chat turns persist the same way.

## Consequences
- No changes to `AIProvider`, `ChatService`, `/chat`, or `PromptBuilder`.
- New files: `app/interfaces/tool.py`, `app/interfaces/tool_calling_provider.py`, `app/tools/rag_search_tool.py`, `app/tools/current_datetime_tool.py`, `app/services/agent_service.py`, `app/dependencies/agent.py`, `app/schemas/agent_schema.py`, `app/api/agent_router.py`.
- `OllamaProvider` gains a `chat()` method alongside `generate()`.
- Adding a new tool means: implement `Tool`, add it to the list in `app/dependencies/agent.py:get_agent_service`. No other wiring needed.
- `MAX_ITERATIONS` is a blunt safety bound, not a cost/latency budget — each iteration is a full model call. Revisit if agents grow more tools or longer chains.
