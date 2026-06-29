from ollama import chat

from app.interfaces.tool_calling_provider import ProviderMessage, ToolCall


class OllamaProvider:
    def generate(self, prompt: str) -> str:

        responses = chat(
            model="qwen3:latest",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return responses.message.content

    def chat(self, messages: list[dict], tools: list[dict]) -> ProviderMessage:

        ollama_messages = [self._to_ollama_message(message) for message in messages]

        response = chat(model="qwen3:latest", messages=ollama_messages, tools=tools)

        tool_calls = [
            ToolCall(name=tool_call.function.name, arguments=dict(tool_call.function.arguments))
            for tool_call in (response.message.tool_calls or [])
        ]

        return ProviderMessage(content=response.message.content, tool_calls=tool_calls)

    def _to_ollama_message(self, message: dict) -> dict:

        if "tool_calls" not in message:
            return message

        return {
            **message,
            "tool_calls": [
                {"function": {"name": tool_call["name"], "arguments": tool_call["arguments"]}}
                for tool_call in message["tool_calls"]
            ],
        }