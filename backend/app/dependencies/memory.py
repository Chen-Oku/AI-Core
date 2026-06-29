from app.memory.database import init_db
from app.memory.session_manager import SessionManager

init_db()

session_manager = SessionManager()


def get_session_manager():

    return session_manager