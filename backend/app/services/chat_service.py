from app.memory.session_manager import SessionManager


class ChatService:

    def __init__(

        self,

        provider,

        prompt_builder,

        session_manager: SessionManager,

        rag_service=None

    ):

        self.provider = provider

        self.prompt_builder = prompt_builder

        self.session_manager = session_manager

        self.rag_service = rag_service

    def ask(self, message: str, session_id: str | None, tenant: str, use_rag: bool = False) -> tuple[str, str]:

        session_id, memory = self.session_manager.get_or_create(session_id, tenant)

        conversation = memory.get_messages()

        context = self.rag_service.retrieve(message, tenant) if use_rag else None

        prompt = self.prompt_builder.build(conversation, message, context)

        response = self.provider.generate(prompt)

        memory.add_user_message(message)

        memory.add_assistant_message(response)

        return response, session_id