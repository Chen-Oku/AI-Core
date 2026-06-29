import uuid


class RagService:

    def __init__(self, embedding_provider, vector_store):

        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def ingest(self, text: str, metadata: dict | None = None) -> str:

        document_id = uuid.uuid4().hex
        embedding = self.embedding_provider.embed(text)

        self.vector_store.add(document_id, text, embedding, metadata)

        return document_id

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:

        embedding = self.embedding_provider.embed(query)
        results = self.vector_store.query(embedding, top_k)

        return [result["text"] for result in results]
