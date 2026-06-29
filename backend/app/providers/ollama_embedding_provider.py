from ollama import embed


class OllamaEmbeddingProvider:

    def __init__(self, model: str):

        self.model = model

    def embed(self, text: str) -> list[float]:

        response = embed(model=self.model, input=text)

        return response.embeddings[0]
