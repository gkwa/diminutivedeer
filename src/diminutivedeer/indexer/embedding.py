import abc


class EmbeddingClient(abc.ABC):
    @abc.abstractmethod
    def embed(self, text: str) -> list[float]:
        """Embed text and return a list of floats representing the embedding vector"""
        pass

    @abc.abstractmethod
    def get_dimension(self) -> int:
        """Return the dimension of the embedding vectors this client produces"""
        pass
