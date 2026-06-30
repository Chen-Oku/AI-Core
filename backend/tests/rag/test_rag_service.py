from app.services.rag_service import RagService


class FakeEmbeddingProvider:

    def embed(self, text: str) -> list[float]:

        return [float(len(text))]


class FakeVectorStore:

    def __init__(self):

        self.added = []
        self.last_where = None

    def add(self, id, text, embedding, metadata=None):

        self.added.append((id, text, embedding, metadata))

    def query(self, embedding, top_k, where=None):

        self.last_where = where

        return [{"text": text, "metadata": metadata, "distance": 0.0} for _, text, _, metadata in self.added[:top_k]]


def test_ingest_embeds_and_stores_the_text():

    vector_store = FakeVectorStore()
    service = RagService(FakeEmbeddingProvider(), vector_store)

    document_id, chunk_count = service.ingest("hello world", "tenant-a", {"source": "test"})

    assert chunk_count == 1
    assert len(vector_store.added) == 1
    stored_id, text, embedding, metadata = vector_store.added[0]
    assert text == "hello world"
    assert embedding == [11.0]
    assert metadata == {"source": "test", "document_id": document_id, "chunk_index": 0, "tenant": "tenant-a"}


def test_ingest_splits_long_text_into_multiple_overlapping_chunks():

    vector_store = FakeVectorStore()
    service = RagService(FakeEmbeddingProvider(), vector_store, chunk_size=10, chunk_overlap=2)

    document_id, chunk_count = service.ingest("a" * 25, "tenant-a")

    assert chunk_count > 1
    assert len(vector_store.added) == chunk_count
    assert {metadata["document_id"] for _, _, _, metadata in vector_store.added} == {document_id}
    assert [metadata["chunk_index"] for _, _, _, metadata in vector_store.added] == list(range(chunk_count))


def test_retrieve_returns_the_matched_texts():

    vector_store = FakeVectorStore()
    service = RagService(FakeEmbeddingProvider(), vector_store)

    service.ingest("first document", "tenant-a")
    service.ingest("second document", "tenant-a")

    assert service.retrieve("a query", "tenant-a", top_k=1) == ["first document"]


def test_retrieve_scopes_the_query_to_the_given_tenant():

    vector_store = FakeVectorStore()
    service = RagService(FakeEmbeddingProvider(), vector_store)

    service.retrieve("a query", "tenant-a")

    assert vector_store.last_where == {"tenant": "tenant-a"}
