import uuid

from sqlalchemy.orm import Session

from app.interfaces.memory import ConversationMemory
from app.memory.sqlalchemy_conversation_memory import SqlAlchemyConversationMemory


class SessionManager:

    def __init__(self, db: Session):

        self.db = db

    def get_or_create(self, session_id: str | None, tenant: str) -> tuple[str, ConversationMemory]:

        resolved_id = session_id or uuid.uuid4().hex

        return resolved_id, SqlAlchemyConversationMemory(self.db, resolved_id, tenant)
