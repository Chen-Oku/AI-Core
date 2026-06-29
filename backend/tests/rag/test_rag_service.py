from app.services.rag_service import RagService


class FakeEmbeddingProvider:

    def embed(self, text: str) -> list[float]:

        return [float(len(text))]


class FakeVectorStore:

    def __init__(self):

        self.added = []

    def add(self, id, text, embedding, metadata=None):

        self.added.append((id, text, embedding, metadata))

    def query(self, embedding, top_k):

        return [{"text": text, "metadata": metadata, "distance": 0.0} for _, text, _, metadata in self.added[:top_k]]


def test_ingest_embeds_and_stores_the_text():

    vector_store = FakeVectorStore()
    service = RagService(FakeEmbeddingProvider(), vector_store)

    document_id = service.ingest("hello world", {"source": "test"})

    assert len(vector_store.added) == 1
    stored_id, text, embedding, metadata = vector_store.added[0]
    assert stored_id == document_id
    assert text == "hello world"
    assert embedding == [11.0]
    assert metadata == {"source": "test"}


def test_retrieve_returns_the_matched_texts():

    vector_store = FakeVectorStore()
    service = RagService(FakeEmbeddingProvider(), vector_store)

    service.ingest("first document")
    service.ingest("second document")

    assert service.retrieve("a query", top_k=1) == ["first document"]
