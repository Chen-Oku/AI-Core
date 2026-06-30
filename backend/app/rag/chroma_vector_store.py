from chromadb.api.models.Collection import Collection


class ChromaVectorStore:

    def __init__(self, collection: Collection):

        self.collection = collection

    def add(self, id: str, text: str, embedding: list[float], metadata: dict | None = None) -> None:

        self.collection.add(
            ids=[id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    def query(self, embedding: list[float], top_k: int, where: dict | None = None) -> list[dict]:

        results = self.collection.query(query_embeddings=[embedding], n_results=top_k, where=where)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        return [
            {"text": text, "metadata": metadata, "distance": distance}
            for text, metadata, distance in zip(documents, metadatas, distances)
        ]
