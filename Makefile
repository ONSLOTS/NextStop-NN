.PHONY: up load-qdrant setup

up:
	docker compose up -d

load-qdrant:
	cd backend && uv run python restore_qdrant_snapshot.py

setup: up load-qdrant

