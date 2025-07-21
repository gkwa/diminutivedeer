# Show available commands
default:
	@just --list

# Build and create sample docs
setup:
	docker compose build
	mkdir -p docs docs2
	echo -e "# Sample Document\n\nThis is a test document for indexing." > docs/sample.md
	echo -e "# Another Document\n\n## Section 1\n\nContent here.\n\n## Section 2\n\nMore content." > docs/another.md
	echo -e "# Third Document\n\nThis is in the second directory." > docs2/third.md

# Run tests and index documents
test:
	docker compose run --rm test
	docker compose run --rm diminutivedeer diminutivedeer index /app/docs /app/docs2 --provider mock --db-path /app/chroma_db

# Run with telemetry disabled
test-no-telemetry:
	docker compose run --rm diminutivedeer diminutivedeer --no-telemetry index /app/docs /app/docs2 --provider mock --db-path /app/chroma_db

# Clean up everything
teardown:
	docker compose down -v
	docker system prune -f
	rm -rf docs/ docs2/ chroma_db/
