from app.tools.rag_search_tool import RagSearchTool


class FakeRagService:

    def __init__(self, chunks):

        self.chunks = chunks
        self.queries = []

    def retrieve(self, query, top_k=3):

        self.queries.append(query)

        return self.chunks


def test_run_joins_the_retrieved_chunks():

    tool = RagSearchTool(FakeRagService(["chunk one", "chunk two"]))

    result = tool.run(query="something")

    assert result == "chunk one\nchunk two"
    assert tool.rag_service.queries == ["something"]


def test_run_reports_when_nothing_is_found():

    tool = RagSearchTool(FakeRagService([]))

    assert tool.run(query="something") == "No relevant information found."
