from app.memory.database import init_db
from app.memory.session_manager import SessionManager


def test_get_or_create_generates_a_new_id_each_time(tmp_path):

    db_path = tmp_path / "conversations.db"
    init_db(db_path)
    manager = SessionManager(db_path)

    first_id, _ = manager.get_or_create(None)
    second_id, _ = manager.get_or_create(None)

    assert first_id != second_id


def test_get_or_create_reuses_a_given_session_id(tmp_path):

    db_path = tmp_path / "conversations.db"
    init_db(db_path)
    manager = SessionManager(db_path)

    session_id, memory = manager.get_or_create("existing-session")
    memory.add_user_message("hello")

    same_id, same_session_memory = manager.get_or_create("existing-session")

    assert session_id == same_id == "existing-session"
    assert same_session_memory.get_messages() == [{"role": "user", "content": "hello"}]
