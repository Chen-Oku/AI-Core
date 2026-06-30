from typing import Protocol


class VectorStore(Protocol):

    def add(self, id: str, text: str, embedding: list[float], metadata: dict | None = None) -> None:
        ...

    def query(self, embedding: list[float], top_k: int, where: dict | None = None) -> list[dict]:
        ...
