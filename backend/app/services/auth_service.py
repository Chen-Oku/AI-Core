import hashlib


class AuthenticationError(Exception):
    pass


class AuthService:

    def __init__(self, repository):

        self.repository = repository

    def authenticate(self, raw_key: str) -> str:

        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        tenant = self.repository.find_active_tenant_by_hash(key_hash)

        if tenant is None:
            raise AuthenticationError("Invalid or inactive API key")

        return tenant
