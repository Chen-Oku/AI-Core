import argparse
import hashlib
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.auth.models import ApiKey
from app.core import db_models  # noqa: F401 -- registers every ORM model with Base.metadata before init_db() runs
from app.core.config import settings
from app.memory.db import create_db_engine, create_session_factory, init_db


def create_api_key(tenant: str) -> str:

    raw_key = secrets.token_urlsafe(32)
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

    engine = create_db_engine(settings.database_url)
    init_db(engine)
    db = create_session_factory(engine)()

    db.add(ApiKey(tenant=tenant, key_hash=key_hash))
    db.commit()
    db.close()

    return raw_key


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create a new AI Core API key for a tenant.")
    parser.add_argument("tenant", help="Tenant/app name, e.g. career-intelligence-platform")
    args = parser.parse_args()

    raw_key = create_api_key(args.tenant)

    print(f"API key for '{args.tenant}': {raw_key}")
    print("Store this now -- only its hash is kept, it cannot be recovered later.")
