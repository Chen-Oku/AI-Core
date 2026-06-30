from typing import Protocol


class ApiKeyRepository(Protocol):

    def find_active_tenant_by_hash(self, key_hash: str) -> str | None:
        ...
