from typing import Protocol


class Tool(Protocol):
    name: str
    description: str
    parameters: dict

    def run(self, **kwargs) -> str:
        ...
