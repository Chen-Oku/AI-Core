import sqlite3
from pathlib import Path

from app.memory.database import DEFAULT_DB_PATH


class SqliteConversationMemory:

    def __init__(self, session_id: str, db_path: Path = DEFAULT_DB_PATH):

        self.session_id = session_id
        self.db_path = db_path

    def add_user_message(self, message: str) -> None:

        self._add_message("user", message)

    def add_assistant_message(self, message: str) -> None:

        self._add_message("assistant", message)

    def get_messages(self) -> list[dict]:

        connection = sqlite3.connect(self.db_path)

        try:
            rows = connection.execute(
                "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id",
                (self.session_id,)
            ).fetchall()
        finally:
            connection.close()

        return [{"role": role, "content": content} for role, content in rows]

    def _add_message(self, role: str, content: str) -> None:

        connection = sqlite3.connect(self.db_path)

        try:
            connection.execute(
                "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
                (self.session_id, role, content)
            )
            connection.commit()
        finally:
            connection.close()
