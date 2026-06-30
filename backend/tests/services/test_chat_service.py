from app.services.chat_service import ChatService


class FakeProvider:

    def generate(self, prompt):

        self.last_prompt = prompt

        return "fake response"


class FakeMemory:

    def __init__(self):

        self.messages = []

    def get_messages(self):

        return self.messages

    def add_user_message(self, message):

        self.messages.append({"role": "user", "content": message})

    def add_assistant_message(self, message):

        self.messages.append({"role": "assistant", "content": message})


class FakeSessionManager:

    def __init__(self):

        self.memory = FakeMemory()

    def get_or_create(self, session_id, tenant):

        self.tenant = tenant

        return session_id or "new-session", self.memory


class FakePromptBuilder:

    def build(self, conversation, message, context=None):

        self.last_context = context

        return "built prompt"


class FakeRagService:

    def __init__(self, chunks):

        self.chunks = chunks
        self.queries = []

    def retrieve(self, query, tenant, top_k=3):

        self.queries.append(query)
        self.tenant = tenant

        return self.chunks


def test_ask_persists_messages_and_returns_response_and_session_id():

    session_manager = FakeSessionManager()
    service = ChatService(FakeProvider(), FakePromptBuilder(), session_manager)

    response, session_id = service.ask("hello", "session-a", "tenant-a")

    assert response == "fake response"
    assert session_id == "session-a"
    assert session_manager.memory.messages == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "fake response"},
    ]


def test_ask_without_rag_does_not_query_the_rag_service():

    prompt_builder = FakePromptBuilder()
    rag_service = FakeRagService(["irrelevant chunk"])
    service = ChatService(FakeProvider(), prompt_builder, FakeSessionManager(), rag_service)

    service.ask("hello", None, "tenant-a", use_rag=False)

    assert rag_service.queries == []
    assert prompt_builder.last_context is None


def test_ask_with_rag_retrieves_context_and_passes_it_to_the_prompt_builder():

    prompt_builder = FakePromptBuilder()
    rag_service = FakeRagService(["relevant chunk"])
    service = ChatService(FakeProvider(), prompt_builder, FakeSessionManager(), rag_service)

    service.ask("hello", None, "tenant-a", use_rag=True)

    assert rag_service.queries == ["hello"]
    assert rag_service.tenant == "tenant-a"
    assert prompt_builder.last_context == ["relevant chunk"]
