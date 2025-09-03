#!/bin/bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --reload-dir app
# uv run gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --workers 1 --reload --reload-dir app
