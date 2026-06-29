from typing import Protocol


class ConversationMemory(Protocol):

    def add_user_message(self, message: str) -> None:
        ...

    def add_assistant_message(self, message: str) -> None:
        ...

    def get_messages(self) -> list[dict]:
        ...
