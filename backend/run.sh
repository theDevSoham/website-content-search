#!/bin/sh
# run.sh
set -e
echo "PORT from env: $PORT"

# Use Render's PORT if set, otherwise default to 8000 for local/dev
PORT=${PORT:-8000}

echo "Starting server on port $PORT..."
exec uv run gunicorn -k uvicorn.workers.UvicornWorker app.main:app \
    --workers 1 \
    --bind 0.0.0.0:$PORT
