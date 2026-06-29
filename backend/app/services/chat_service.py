from app.memory.session_manager import SessionManager


class ChatService:

    def __init__(

        self,

        provider,

        prompt_builder,

        session_manager: SessionManager

    ):

        self.provider = provider

        self.prompt_builder = prompt_builder

        self.session_manager = session_manager

    def ask(self, message: str, session_id: str | None) -> tuple[str, str]:

        session_id, memory = self.session_manager.get_or_create(session_id)

        conversation = memory.get_messages()

        prompt = self.prompt_builder.build(conversation, message)

        response = self.provider.generate(prompt)

        memory.add_user_message(message)

        memory.add_assistant_message(response)

        return response, session_id