import argparse
import chromadb
import chromadb.config
import hashlib
import logging
import os
import re
import sys


def configure_telemetry(disable_telemetry):
    """Configure ChromaDB telemetry settings"""
    if disable_telemetry:
        # Disable ChromaDB telemetry
        os.environ["ANONYMIZED_TELEMETRY"] = "FALSE"
        # Suppress telemetry error messages (known ChromaDB bug)
        logging.getLogger("chromadb.telemetry.product.posthog").setLevel(
            logging.CRITICAL
        )
    else:
        # Enable telemetry (ChromaDB default)
        os.environ["ANONYMIZED_TELEMETRY"] = "TRUE"


def chunk_markdown(text, max_tokens=500):
    """Markdown-aware chunking that preserves structure"""
    # Split by headers first
    sections = re.split(r"^(#{1,6}\s+.+)$", text, flags=re.MULTILINE)

    chunks = []
    current_chunk = []
    current_tokens = 0
    current_header = ""

    for i, section in enumerate(sections):
        if not section.strip():
            continue

        # Check if this is a header
        if re.match(r"^#{1,6}\s+", section):
            # If we have content, finalize the current chunk
            if current_chunk:
                chunk_text = (
                    current_header + "\n\n" + "\n".join(current_chunk)
                ).strip()
                chunks.append(chunk_text)
                current_chunk = []
                current_tokens = 0

            current_header = section
        else:
            # Split content by paragraphs
            paragraphs = [p.strip() for p in section.split("\n\n") if p.strip()]

            for para in paragraphs:
                para_tokens = len(para.split())

                if current_tokens + para_tokens > max_tokens and current_chunk:
                    # Finalize current chunk
                    chunk_text = (
                        current_header + "\n\n" + "\n".join(current_chunk)
                    ).strip()
                    chunks.append(chunk_text)
                    current_chunk = [para]
                    current_tokens = para_tokens
                else:
                    current_chunk.append(para)
                    current_tokens += para_tokens

    # Add final chunk
    if current_chunk:
        chunk_text = (current_header + "\n\n" + "\n".join(current_chunk)).strip()
        chunks.append(chunk_text)

    return chunks if chunks else [text]


def process_markdown_file(path, collection, embedder):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_markdown(text)

    for i, chunk in enumerate(chunks):
        embedding = embedder.embed(chunk)
        doc_id = hashlib.sha256(f"{path}-{i}".encode()).hexdigest()

        collection.add(
            ids=[doc_id],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"source": path, "chunk": i, "total_chunks": len(chunks)}],
        )
        print(f"Indexed: {path} [chunk {i + 1}/{len(chunks)}]")


def index_directories(directories, chroma_path, embedder, disable_telemetry):
    # Create ChromaDB client with telemetry settings
    chroma_client = chromadb.PersistentClient(
        path=chroma_path,
        settings=chromadb.config.Settings(anonymized_telemetry=not disable_telemetry),
    )
    collection = chroma_client.get_or_create_collection("markdown_docs")

    markdown_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".md"):
                    markdown_files.append(os.path.join(root, file))

    print(
        f"Found {len(markdown_files)} markdown files to index across {len(directories)} directories..."
    )

    for file_path in markdown_files:
        process_markdown_file(file_path, collection, embedder)

    print(
        f"Indexing complete! Processed {len(markdown_files)} files from {len(directories)} directories."
    )


def run_index(args):
    """Run the index command with parsed arguments"""
    # Configure telemetry based on user preference
    configure_telemetry(args.no_telemetry)

    # Validate that all directories exist
    for docs_dir in args.docs_dirs:
        if not os.path.exists(docs_dir):
            print(f"Error: Directory {docs_dir} does not exist")
            sys.exit(1)

    # Initialize embedder based on provider
    if args.provider == "openai":
        import diminutivedeer.indexer.providers.openai

        model = args.model or "text-embedding-3-small"
        embedder = diminutivedeer.indexer.providers.openai.OpenAIEmbedder(model=model)
    elif args.provider == "claude":
        import diminutivedeer.indexer.providers.claude

        model = args.model or "claude-3-haiku-20240307"
        embedder = diminutivedeer.indexer.providers.claude.ClaudeEmbedder(model=model)
    else:  # mock
        import diminutivedeer.indexer.providers.mock

        embedder = diminutivedeer.indexer.providers.mock.MockEmbedder()

    print(f"Using {args.provider} embedder with dimension {embedder.get_dimension()}")
    if args.no_telemetry:
        print("Telemetry disabled")

    index_directories(args.docs_dirs, args.db_path, embedder, args.no_telemetry)


def main():
    """Legacy entry point for backwards compatibility"""
    parser = argparse.ArgumentParser(
        description="Index markdown documents using embeddings"
    )
    parser.add_argument(
        "docs_dirs", nargs="+", help="Directories containing markdown files to index"
    )
    parser.add_argument(
        "--db-path", default="./chroma_db", help="Path for ChromaDB storage"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "mock", "claude"],
        default="mock",
        help="Embedding provider to use",
    )
    parser.add_argument("--model", help="Model name for the embedding provider")
    parser.add_argument(
        "--max-tokens", type=int, default=500, help="Maximum tokens per chunk"
    )
    parser.add_argument(
        "--no-telemetry",
        action="store_true",
        help="Disable anonymous telemetry data collection",
    )

    args = parser.parse_args()
    run_index(args)


if __name__ == "__main__":
    main()
