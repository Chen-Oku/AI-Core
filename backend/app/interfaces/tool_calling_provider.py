from dataclasses import dataclass
from typing import Protocol


@dataclass
class ToolCall:
    name: str
    arguments: dict


@dataclass
class ProviderMessage:
    content: str | None
    tool_calls: list[ToolCall]


class ToolCallingProvider(Protocol):

    def chat(self, messages: list[dict], tools: list[dict]) -> ProviderMessage:
        ...
