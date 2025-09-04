# 1. Base image
FROM python:3.11-slim

# 2. Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 4. Set work directory
WORKDIR /app

# 3. Copy the application into the container.
COPY backend/ .  

# 5. Install dependencies with uv
RUN uv sync --frozen --no-cache

# 6. Expose the port (Render auto-detects $PORT)
EXPOSE 8000

# 7. Run with Gunicorn + Uvicorn workers
CMD uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
