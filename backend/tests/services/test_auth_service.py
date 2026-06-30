import hashlib

import pytest

from app.services.auth_service import AuthenticationError, AuthService


class FakeApiKeyRepository:

    def __init__(self, hash_to_tenant: dict):

        self.hash_to_tenant = hash_to_tenant

    def find_active_tenant_by_hash(self, key_hash):

        return self.hash_to_tenant.get(key_hash)


def test_authenticate_returns_the_tenant_for_a_known_key():

    raw_key = "secret-key"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    repository = FakeApiKeyRepository({key_hash: "career-intelligence-platform"})
    service = AuthService(repository)

    assert service.authenticate(raw_key) == "career-intelligence-platform"


def test_authenticate_raises_for_an_unknown_key():

    service = AuthService(FakeApiKeyRepository({}))

    with pytest.raises(AuthenticationError):
        service.authenticate("unknown-key")
