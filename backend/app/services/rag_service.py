import uuid

from app.rag.chunker import split_text


class RagService:

    def __init__(self, embedding_provider, vector_store, chunk_size: int = 500, chunk_overlap: int = 50):

        self.embedding_provider = embedding_provider
        self.vector_store = vector_store
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def ingest(self, text: str, tenant: str, metadata: dict | None = None) -> tuple[str, int]:

        document_id = uuid.uuid4().hex
        chunks = split_text(text, self.chunk_size, self.chunk_overlap)

        for index, chunk in enumerate(chunks):

            chunk_id = uuid.uuid4().hex
            embedding = self.embedding_provider.embed(chunk)
            chunk_metadata = {**(metadata or {}), "document_id": document_id, "chunk_index": index, "tenant": tenant}

            self.vector_store.add(chunk_id, chunk, embedding, chunk_metadata)

        return document_id, len(chunks)

    def retrieve(self, query: str, tenant: str, top_k: int = 3) -> list[str]:

        embedding = self.embedding_provider.embed(query)
        results = self.vector_store.query(embedding, top_k, where={"tenant": tenant})

        return [result["text"] for result in results]
