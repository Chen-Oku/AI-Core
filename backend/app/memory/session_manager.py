import uuid
from pathlib import Path

from app.interfaces.memory import ConversationMemory
from app.memory.database import DEFAULT_DB_PATH
from app.memory.sqlite_conversation_memory import SqliteConversationMemory


class SessionManager:

    def __init__(self, db_path: Path = DEFAULT_DB_PATH):

        self.db_path = db_path

    def get_or_create(self, session_id: str | None) -> tuple[str, ConversationMemory]:

        resolved_id = session_id or uuid.uuid4().hex

        return resolved_id, SqliteConversationMemory(resolved_id, self.db_path)
