from app.auth.models import ApiKey
from app.auth.sqlalchemy_api_key_repository import SqlAlchemyApiKeyRepository
from app.memory.db import create_db_engine, create_session_factory, init_db


def _make_session(tmp_path):

    engine = create_db_engine(f"sqlite:///{tmp_path / 'auth.db'}")
    init_db(engine)

    return create_session_factory(engine)()


def test_find_active_tenant_by_hash_returns_the_tenant(tmp_path):

    db = _make_session(tmp_path)
    db.add(ApiKey(key_hash="hash-a", tenant="tenant-a", is_active=True))
    db.commit()

    repository = SqlAlchemyApiKeyRepository(db)

    assert repository.find_active_tenant_by_hash("hash-a") == "tenant-a"


def test_find_active_tenant_by_hash_returns_none_for_an_unknown_hash(tmp_path):

    db = _make_session(tmp_path)
    repository = SqlAlchemyApiKeyRepository(db)

    assert repository.find_active_tenant_by_hash("missing-hash") is None


def test_find_active_tenant_by_hash_ignores_inactive_keys(tmp_path):

    db = _make_session(tmp_path)
    db.add(ApiKey(key_hash="hash-b", tenant="tenant-b", is_active=False))
    db.commit()

    repository = SqlAlchemyApiKeyRepository(db)

    assert repository.find_active_tenant_by_hash("hash-b") is None
