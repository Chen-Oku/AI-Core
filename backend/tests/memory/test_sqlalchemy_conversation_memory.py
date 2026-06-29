from app.memory.db import create_db_engine, create_session_factory, init_db
from app.memory.sqlalchemy_conversation_memory import SqlAlchemyConversationMemory


def _make_session_factory(tmp_path):

    engine = create_db_engine(f"sqlite:///{tmp_path / 'conversations.db'}")
    init_db(engine)

    return create_session_factory(engine)


def test_messages_persist_across_instances(tmp_path):

    session_factory = _make_session_factory(tmp_path)

    first = SqlAlchemyConversationMemory(session_factory(), "session-a")
    first.add_user_message("hello")
    first.add_assistant_message("hi there")

    second = SqlAlchemyConversationMemory(session_factory(), "session-a")

    assert second.get_messages() == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi there"},
    ]


def test_sessions_are_isolated(tmp_path):

    session_factory = _make_session_factory(tmp_path)

    session_a = SqlAlchemyConversationMemory(session_factory(), "session-a")
    session_b = SqlAlchemyConversationMemory(session_factory(), "session-b")

    session_a.add_user_message("only in a")

    assert session_a.get_messages() == [{"role": "user", "content": "only in a"}]
    assert session_b.get_messages() == []
