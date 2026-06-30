from fastapi import Depends
from sqlalchemy.orm import Session

from app.core import db_models  # noqa: F401 -- registers every ORM model with Base.metadata before init_db() runs
from app.core.config import settings
from app.memory.db import create_db_engine, create_session_factory, init_db
from app.memory.session_manager import SessionManager

engine = create_db_engine(settings.database_url)
init_db(engine)
SessionFactory = create_session_factory(engine)


def get_db():

    db = SessionFactory()

    try:
        yield db
    finally:
        db.close()


def get_session_manager(db: Session = Depends(get_db)) -> SessionManager:

    return SessionManager(db)
