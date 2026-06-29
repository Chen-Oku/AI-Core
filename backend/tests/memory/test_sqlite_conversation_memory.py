from app.memory.database import init_db
from app.memory.sqlite_conversation_memory import SqliteConversationMemory


def test_messages_persist_across_instances(tmp_path):

    db_path = tmp_path / "conversations.db"
    init_db(db_path)

    first = SqliteConversationMemory("session-a", db_path)
    first.add_user_message("hello")
    first.add_assistant_message("hi there")

    second = SqliteConversationMemory("session-a", db_path)

    assert second.get_messages() == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi there"},
    ]


def test_sessions_are_isolated(tmp_path):

    db_path = tmp_path / "conversations.db"
    init_db(db_path)

    session_a = SqliteConversationMemory("session-a", db_path)
    session_b = SqliteConversationMemory("session-b", db_path)

    session_a.add_user_message("only in a")

    assert session_a.get_messages() == [{"role": "user", "content": "only in a"}]
    assert session_b.get_messages() == []
