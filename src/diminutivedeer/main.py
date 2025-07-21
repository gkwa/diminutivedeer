import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="diminutivedeer - Document indexing and embedding system with ChromaDB",
        prog="diminutivedeer",
    )

    # Global arguments
    parser.add_argument(
        "--no-telemetry",
        action="store_true",
        help="Disable anonymous telemetry data collection",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Index subcommand
    index_parser = subparsers.add_parser("index", help="Index markdown documents")
    index_parser.add_argument(
        "docs_dirs", nargs="+", help="Directories containing markdown files to index"
    )
    index_parser.add_argument(
        "--db-path", default="./chroma_db", help="Path for ChromaDB storage"
    )
    index_parser.add_argument(
        "--provider",
        choices=["openai", "mock", "claude"],
        default="mock",
        help="Embedding provider to use",
    )
    index_parser.add_argument("--model", help="Model name for the embedding provider")
    index_parser.add_argument(
        "--max-tokens", type=int, default=500, help="Maximum tokens per chunk"
    )
    index_parser.add_argument(
        "--no-telemetry",
        action="store_true",
        help="Disable anonymous telemetry data collection",
    )

    args = parser.parse_args()

    if args.command == "index":
        import diminutivedeer.indexer.main
        diminutivedeer.indexer.main.run_index(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
