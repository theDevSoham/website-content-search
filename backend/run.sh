#!/bin/sh
# run.sh

# Use Render's PORT if set, otherwise default to 8000 for local/dev
PORT=${PORT:-8000}

echo "Starting server on port $PORT..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT
