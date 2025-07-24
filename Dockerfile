FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Suppress UV hardlink warnings in Docker
ENV UV_LINK_MODE=copy

# Copy only dependency files first for better caching
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies only (not the project itself) for better caching
RUN uv sync --frozen --no-install-project

# Copy project files (this happens after dependency installation)
COPY README.md ./
COPY src/diminutivedeer ./src/diminutivedeer
COPY tests/ ./tests/

# Install the project and all dependencies
RUN uv sync --frozen

# Make the virtual environment the default Python environment
ENV PATH="/app/.venv/bin:$PATH"

CMD ["diminutivedeer"]
