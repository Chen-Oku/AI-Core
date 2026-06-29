from app.interfaces.tool_calling_provider import ProviderMessage, ToolCall
from app.services.agent_service import AgentService


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

    def get_or_create(self, session_id):

        return session_id or "new-session", self.memory


class FakeProvider:

    def __init__(self, responses):

        self.responses = list(responses)
        self.calls = []

    def chat(self, messages, tools):

        self.calls.append((messages, tools))

        return self.responses.pop(0)


class FakeTool:

    name = "echo"
    description = "Echoes the input back"
    parameters = {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}

    def __init__(self):

        self.calls = []

    def run(self, text):

        self.calls.append(text)

        return f"echo: {text}"


def test_ask_returns_the_final_answer_when_no_tool_is_called():

    provider = FakeProvider([ProviderMessage(content="hi there", tool_calls=[])])
    service = AgentService(provider, [FakeTool()], FakeSessionManager())

    response, session_id = service.ask("hello", "session-a")

    assert response == "hi there"
    assert session_id == "session-a"


def test_ask_executes_a_tool_call_and_feeds_the_result_back():

    tool = FakeTool()
    provider = FakeProvider([
        ProviderMessage(content="", tool_calls=[ToolCall(name="echo", arguments={"text": "hello"})]),
        ProviderMessage(content="final answer", tool_calls=[]),
    ])
    service = AgentService(provider, [tool], FakeSessionManager())

    response, _ = service.ask("say hello", None)

    assert response == "final answer"
    assert tool.calls == ["hello"]

    second_call_messages = provider.calls[1][0]
    assert second_call_messages[-1] == {"role": "tool", "content": "echo: hello", "tool_name": "echo"}


def test_ask_stops_after_max_iterations_of_repeated_tool_calls():

    tool = FakeTool()
    always_calls_tool = ProviderMessage(content="", tool_calls=[ToolCall(name="echo", arguments={"text": "x"})])
    provider = FakeProvider([always_calls_tool] * 5)
    service = AgentService(provider, [tool], FakeSessionManager())

    response, _ = service.ask("loop forever", None)

    assert "Could not complete" in response
    assert len(provider.calls) == 5


def test_ask_persists_user_and_assistant_messages():

    session_manager = FakeSessionManager()
    provider = FakeProvider([ProviderMessage(content="answer", tool_calls=[])])
    service = AgentService(provider, [], session_manager)

    service.ask("question", "session-a")

    assert session_manager.memory.messages == [
        {"role": "user", "content": "question"},
        {"role": "assistant", "content": "answer"},
    ]
