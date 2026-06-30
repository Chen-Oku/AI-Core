from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app.core.db_base import Base


class ApiKey(Base):

    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key_hash = Column(String, nullable=False, unique=True, index=True)
    tenant = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
