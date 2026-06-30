from sqlalchemy import select
from sqlalchemy.orm import Session

from app.memory.models import Message


class SqlAlchemyConversationMemory:

    def __init__(self, db: Session, session_id: str, tenant: str):

        self.db = db
        self.session_id = session_id
        self.tenant = tenant

    def add_user_message(self, message: str) -> None:

        self._add_message("user", message)

    def add_assistant_message(self, message: str) -> None:

        self._add_message("assistant", message)

    def get_messages(self) -> list[dict]:

        rows = self.db.execute(
            select(Message.role, Message.content)
            .where(Message.session_id == self.session_id, Message.tenant == self.tenant)
            .order_by(Message.id)
        ).all()

        return [{"role": role, "content": content} for role, content in rows]

    def _add_message(self, role: str, content: str) -> None:

        self.db.add(Message(session_id=self.session_id, tenant=self.tenant, role=role, content=content))
        self.db.commit()
