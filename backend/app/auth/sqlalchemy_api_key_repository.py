from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.models import ApiKey


class SqlAlchemyApiKeyRepository:

    def __init__(self, db: Session):

        self.db = db

    def find_active_tenant_by_hash(self, key_hash: str) -> str | None:

        return self.db.execute(
            select(ApiKey.tenant).where(ApiKey.key_hash == key_hash, ApiKey.is_active.is_(True))
        ).scalar_one_or_none()
