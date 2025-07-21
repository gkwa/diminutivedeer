# diminutivedeer

A document indexing and embedding system built with ChromaDB.

## Features

- Index markdown documents with intelligent chunking
- Support for multiple embedding providers (OpenAI, mock, Claude placeholder)
- Markdown-aware chunking that preserves document structure
- ChromaDB integration for vector storage and retrieval
- Docker support for cross-platform compatibility
- Multi-directory indexing support
- Configurable telemetry (enabled by default, can be disabled)

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed

### Build and Run

```bash
# Build the Docker image
docker compose build

# Create sample documents (optional)
mkdir -p docs docs2
echo "# Sample Document" > docs/sample.md
echo "# Another Document" > docs2/another.md

# Index documents using mock embedder (no API key needed)
docker compose run --rm diminutivedeer diminutivedeer index /app/docs --provider mock

# Or run tests
docker compose run --rm test

# Get an interactive shell
docker compose run --rm dev bash
```

## Usage Examples

### Getting Help

```bash
# Main help (shows available subcommands)
docker compose run --rm diminutivedeer diminutivedeer --help

# Index subcommand help
docker compose run --rm diminutivedeer diminutivedeer index --help

# Using Docker directly
docker run --rm diminutivedeer diminutivedeer --help
```

### Basic Indexing

```bash
# Using Docker Compose
# Index a single directory with mock embedder (no API key needed)
docker compose run --rm diminutivedeer diminutivedeer index /app/docs --provider mock

# Index multiple directories
docker compose run --rm diminutivedeer diminutivedeer index /app/docs /app/docs2 --provider mock

# Custom database path and chunk size
docker compose run --rm diminutivedeer diminutivedeer index /app/docs --db-path /app/custom_db --max-tokens 300

# Disable telemetry
docker compose run --rm diminutivedeer diminutivedeer --no-telemetry index /app/docs --provider mock

# Using Docker directly
# Index documents from your local directory
docker run --rm \
  -v /path/to/your/docs:/app/docs:ro \
  -v ./chroma_db:/app/chroma_db \
  diminutivedeer diminutivedeer index /app/docs --provider mock

# Index multiple local directories
docker run --rm \
  -v /path/to/docs1:/app/docs1:ro \
  -v /path/to/docs2:/app/docs2:ro \
  -v ./chroma_db:/app/chroma_db \
  diminutivedeer diminutivedeer index /app/docs1 /app/docs2 --provider mock
```

### Using Different Providers

```bash
# Using Docker Compose with OpenAI (set OPENAI_API_KEY environment variable first)
export OPENAI_API_KEY=your_key_here
docker compose run --rm diminutivedeer diminutivedeer index /app/docs --provider openai --model text-embedding-3-small

# Using Docker directly with OpenAI
docker run --rm \
  -e OPENAI_API_KEY=your_key_here \
  -v /path/to/your/docs:/app/docs:ro \
  -v ./chroma_db:/app/chroma_db \
  diminutivedeer diminutivedeer index /app/docs --provider openai --model text-embedding-3-small

# Using Claude placeholder (not yet available via public API)
docker compose run --rm diminutivedeer diminutivedeer index /app/docs --provider claude --model claude-3-haiku-20240307

# Using Docker directly with Claude
docker run --rm \
  -e ANTHROPIC_API_KEY=your_key_here \
  -v /path/to/your/docs:/app/docs:ro \
  -v ./chroma_db:/app/chroma_db \
  diminutivedeer diminutivedeer index /app/docs --provider claude

# Using mock with custom settings
docker compose run --rm diminutivedeer diminutivedeer index /app/docs /app/docs2 --provider mock --max-tokens 500
```

### Development Workflow

```bash
# Start development environment
docker compose run --rm dev bash

# Run tests
docker compose run --rm test

# Build and test with sample docs (requires just command)
just setup
just test

# Test with telemetry disabled
just test-no-telemetry

# Clean up
just teardown
```

### Advanced Docker Usage

```bash
# Build the image with a custom tag
docker build -t my-diminutivedeer .

# Run with custom image
docker run --rm \
  -v /path/to/docs:/app/docs:ro \
  -v ./chroma_db:/app/chroma_db \
  my-diminutivedeer diminutivedeer index /app/docs --provider mock

# Run in background and check logs
docker compose up -d diminutivedeer
docker compose logs -f diminutivedeer

# Mount multiple directories for complex setups
docker run --rm \
  -v /path/to/project-docs:/app/project:ro \
  -v /path/to/api-docs:/app/api:ro \
  -v /path/to/user-guides:/app/guides:ro \
  -v ./chroma_db:/app/chroma_db \
  diminutivedeer diminutivedeer index /app/project /app/api /app/guides --provider mock --max-tokens 800
```

### Mounting Your Own Documents

To index your own documents, mount them as volumes:

```bash
# Single directory
docker run --rm \
  -v /path/to/your/docs:/app/mydocs:ro \
  -v ./chroma_db:/app/chroma_db \
  diminutivedeer diminutivedeer index /app/mydocs --provider mock

# Multiple directories
docker run --rm \
  -v /home/user/project-docs:/app/project:ro \
  -v /home/user/wiki:/app/wiki:ro \
  -v ./chroma_db:/app/chroma_db \
  diminutivedeer diminutivedeer index /app/project /app/wiki --provider mock
```

Or modify `docker-compose.yml` to add your directories:

```yaml
services:
  diminutivedeer:
    build: .
    volumes:
      - ./docs:/app/docs:ro
      - /path/to/your/docs:/app/mydocs:ro  # Add your directory
      - /another/path:/app/more-docs:ro    # Add another directory
      - ./chroma_db:/app/chroma_db
    command: diminutivedeer index /app/docs /app/mydocs /app/more-docs --provider mock
```

## Command Line Options

### Main Command

```
usage: diminutivedeer [-h] [--no-telemetry] {index} ...

diminutivedeer - Document indexing and embedding system with ChromaDB

options:
  -h, --help       show this help message and exit
  --no-telemetry   Disable anonymous telemetry data collection

Available commands:
  {index}
    index          Index markdown documents
```

### Index Subcommand

```
usage: diminutivedeer index [-h] [--db-path DB_PATH] [--provider {openai,mock,claude}] [--model MODEL] [--max-tokens MAX_TOKENS] docs_dirs [docs_dirs ...]

positional arguments:
  docs_dirs             Directories containing markdown files to index

options:
  -h, --help            show this help message and exit
  --db-path DB_PATH     Path for ChromaDB storage (default: ./chroma_db)
  --provider {openai,mock,claude}
                        Embedding provider to use (default: mock)
  --model MODEL         Model name for the embedding provider
  --max-tokens MAX_TOKENS
                        Maximum tokens per chunk (default: 500)
```

## Providers

- **mock**: Deterministic fake embeddings for testing (no API key required)
- **openai**: OpenAI embedding models (requires OPENAI_API_KEY)
  - Available models: `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`
- **claude**: Placeholder for Claude embeddings (not yet available via public API)

## Environment Variables

```bash
# Required for OpenAI provider
export OPENAI_API_KEY=your_openai_api_key

# Required for Claude provider (when available)
export ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Telemetry

By default, diminutivedeer enables ChromaDB's anonymous telemetry to help improve the product. You can disable this with the `--no-telemetry` flag:

```bash
# Disable telemetry for a single run
docker compose run --rm diminutivedeer diminutivedeer --no-telemetry index /app/docs --provider mock

# Or set environment variable to disable globally
export ANONYMIZED_TELEMETRY=FALSE
```

No personally identifiable information is collected. See [ChromaDB's telemetry documentation](https://docs.trychroma.com/telemetry) for details.

## Local Installation (Alternative)

If you prefer to run without Docker:

```bash
# Install the package
pip install -e .

# Or with development dependencies
pip install -e .[dev]

# Then use directly
diminutivedeer index ./docs --provider mock
diminutivedeer index ./docs ./more-docs --provider mock --max-tokens 300
diminutivedeer --no-telemetry index ./docs --provider mock
```

## Project Structure

```
diminutivedeer/
├── src/diminutivedeer/          # Main package
│   ├── main.py                  # Main CLI entry point
│   ├── indexer/                 # Indexing functionality
│   │   ├── main.py             # Index subcommand implementation
│   │   ├── embedding.py        # Embedding interface
│   │   └── providers/          # Embedding providers
│   │       ├── openai.py       # OpenAI embeddings
│   │       ├── claude.py       # Claude embeddings (placeholder)
│   │       └── mock.py         # Mock embeddings for testing
├── tests/                      # Test files
├── docs/                       # Sample documents
├── docs2/                      # Additional sample documents
├── chroma_db/                  # ChromaDB storage (created at runtime)
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose services
├── justfile                    # Convenience commands
└── pyproject.toml              # Project configuration
```

## Tips

- Use the mock provider for testing and development - it's fast and doesn't require API keys
- The system preserves markdown structure during chunking, keeping headers with their content
- ChromaDB persists data in the `chroma_db` directory - you can reuse the same database across runs
- Multiple directories are indexed into the same collection, allowing cross-directory search
- Use `--max-tokens` to control chunk size based on your embedding model's context window
- When using Docker directly, always mount your document directories as read-only (`:ro`) for safety
- Mount the database directory as read-write so ChromaDB can persist your index
- Use `--no-telemetry` if you prefer to disable anonymous usage analytics
- The `index` subcommand structure allows for future expansion with commands like `search` or `query`
```

Key changes made:
1. **Updated all command examples** to use `diminutivedeer index` instead of `diminutivedeer-index`
2. **Added telemetry section** explaining the default behavior and how to disable it
3. **Updated command line help** to show the new subcommand structure
4. **Added examples** showing the `--no-telemetry` flag usage
5. **Updated project structure** to reflect the new main.py organization
6. **Added note about future expansion** with other subcommands

Now the README accurately reflects the current CLI structure!
