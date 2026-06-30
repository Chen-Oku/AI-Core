from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.memory.db import create_db_engine, create_session_factory
from app.memory.session_manager import SessionManager

engine = create_db_engine(settings.database_url)
SessionFactory = create_session_factory(engine)


def get_db():

    db = SessionFactory()

    try:
        yield db
    finally:
        db.close()


def get_session_manager(db: Session = Depends(get_db)) -> SessionManager:

    return SessionManager(db)
