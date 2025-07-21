import anthropic
import diminutivedeer.indexer.embedding
import hashlib
import random


class ClaudeEmbedder(diminutivedeer.indexer.embedding.EmbeddingClient):
    def __init__(self, model: str):
        self.client = anthropic.Anthropic()
        self.model = model
        self._dimension = 1536  # Standard dimension for compatibility

    def embed(self, text: str) -> list[float]:
        # Placeholder: Claude API currently does not support public embeddings
        # Replace this with a real call once available
        h = hashlib.sha256(text.encode()).digest()
        random.seed(int.from_bytes(h[:4], byteorder="big"))
        return [random.uniform(-1, 1) for _ in range(self._dimension)]

    def get_dimension(self) -> int:
        return self._dimension
