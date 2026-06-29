from app.memory.conversation_memory import ConversationMemory


class ChatService:

    def __init__(

        self,

        provider,

        prompt_builder,

        memory: ConversationMemory

    ):

        self.provider = provider

        self.prompt_builder = prompt_builder

        self.memory = memory

    def ask(self, message: str) -> str:

        conversation = self.memory.get_messages()

        prompt = self.prompt_builder.build(conversation, message)

        response = self.provider.generate(prompt)

        self.memory.add_user_message(message)

        self.memory.add_assistant_message(response)

        return response