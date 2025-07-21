import openai
import diminutivedeer.indexer.embedding


class OpenAIEmbedder(diminutivedeer.indexer.embedding.EmbeddingClient):
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = openai.Client()
        self.model = model

        # Set dimensions based on model
        self._dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding

    def get_dimension(self) -> int:
        return self._dimensions.get(self.model, 1536)
