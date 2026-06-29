from typing import Protocol


class ImageProvider(Protocol):

    def generate(self, prompt: str) -> str:
        ...
