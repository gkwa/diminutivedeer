import diminutivedeer.indexer.embedding
import hashlib
import random


class MockEmbedder(diminutivedeer.indexer.embedding.EmbeddingClient):
    """Mock embedder for testing - creates deterministic fake embeddings"""

    def __init__(self, dimension: int = 1536):
        self._dimension = dimension

    def embed(self, text: str) -> list[float]:
        # Create deterministic embeddings based on text hash
        h = hashlib.sha256(text.encode()).digest()
        random.seed(int.from_bytes(h[:4], byteorder="big"))

        # Generate normalized vector for better similarity testing
        vector = [random.gauss(0, 1) for _ in range(self._dimension)]

        # Normalize to unit vector
        magnitude = sum(x * x for x in vector) ** 0.5
        if magnitude > 0:
            vector = [x / magnitude for x in vector]

        return vector

    def get_dimension(self) -> int:
        return self._dimension
