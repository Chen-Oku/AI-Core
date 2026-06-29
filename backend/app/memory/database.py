import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "conversations.db"


def init_db(db_path: Path = DEFAULT_DB_PATH) -> None:

    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        connection.commit()
    finally:
        connection.close()
