from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.core.db_base import Base


def create_db_engine(database_url: str) -> Engine:

    return create_engine(database_url)


def init_db(engine: Engine) -> None:

    Base.metadata.create_all(bind=engine)


def create_session_factory(engine: Engine) -> sessionmaker:

    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
