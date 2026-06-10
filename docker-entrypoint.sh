#!/bin/bash
set -e

echo "Running DB migrations..."
uv run alembic upgrade head

echo "Seeding dummy users..."
uv run python -m app.seed.seed_dummy_users

echo "Starting server..."
exec uv run uvicorn main:app --host 0.0.0.0 --port 8000