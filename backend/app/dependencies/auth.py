from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.sqlalchemy_api_key_repository import SqlAlchemyApiKeyRepository
from app.dependencies.memory import get_db
from app.services.auth_service import AuthenticationError, AuthService


def get_api_key_repository(db: Session = Depends(get_db)) -> SqlAlchemyApiKeyRepository:

    return SqlAlchemyApiKeyRepository(db)


def get_auth_service(
    repository: SqlAlchemyApiKeyRepository = Depends(get_api_key_repository),
) -> AuthService:

    return AuthService(repository)


def get_current_tenant(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    auth_service: AuthService = Depends(get_auth_service),
) -> str:

    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing X-API-Key header")

    try:
        return auth_service.authenticate(x_api_key)
    except AuthenticationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
