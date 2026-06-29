from app.memory.db import create_db_engine, create_session_factory, init_db
from app.memory.session_manager import SessionManager


def _make_manager(tmp_path):

    engine = create_db_engine(f"sqlite:///{tmp_path / 'conversations.db'}")
    init_db(engine)
    db = create_session_factory(engine)()

    return SessionManager(db)


def test_get_or_create_generates_a_new_id_each_time(tmp_path):

    manager = _make_manager(tmp_path)

    first_id, _ = manager.get_or_create(None)
    second_id, _ = manager.get_or_create(None)

    assert first_id != second_id


def test_get_or_create_reuses_a_given_session_id(tmp_path):

    manager = _make_manager(tmp_path)

    session_id, memory = manager.get_or_create("existing-session")
    memory.add_user_message("hello")

    same_id, same_session_memory = manager.get_or_create("existing-session")

    assert session_id == same_id == "existing-session"
    assert same_session_memory.get_messages() == [{"role": "user", "content": "hello"}]
