import os
import sys
import unittest

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import diminutivedeer.indexer.providers.claude
import diminutivedeer.indexer.providers.mock


class TestEmbedders(unittest.TestCase):
    def test_mock_embedder_deterministic(self):
        embedder = diminutivedeer.indexer.providers.mock.MockEmbedder(dimension=128)

        # Same text should produce same embedding
        text = "This is a test document"
        embedding1 = embedder.embed(text)
        embedding2 = embedder.embed(text)

        self.assertEqual(embedding1, embedding2)
        self.assertEqual(len(embedding1), 128)
        self.assertEqual(embedder.get_dimension(), 128)

    def test_mock_embedder_different_texts(self):
        embedder = diminutivedeer.indexer.providers.mock.MockEmbedder(dimension=64)

        embedding1 = embedder.embed("First document")
        embedding2 = embedder.embed("Second document")

        self.assertNotEqual(embedding1, embedding2)
        self.assertEqual(len(embedding1), len(embedding2))

    def test_embedder_interface(self):
        # Test that all embedders implement the interface correctly
        embedders = [
            diminutivedeer.indexer.providers.mock.MockEmbedder(128),
            diminutivedeer.indexer.providers.claude.ClaudeEmbedder(
                "claude-3-haiku-20240307"
            ),
        ]

        for embedder in embedders:
            text = "Test text for embedding"
            embedding = embedder.embed(text)

            self.assertIsInstance(embedding, list)
            self.assertTrue(all(isinstance(x, float) for x in embedding))
            self.assertEqual(len(embedding), embedder.get_dimension())


if __name__ == "__main__":
    unittest.main()
