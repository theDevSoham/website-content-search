# 1. Base image
FROM python:3.11-slim

# 2. Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 4. Set work directory
WORKDIR /app

# 3. Copy the application into the container.
COPY ./ .

# 5. Install dependencies with uv
RUN uv sync --frozen --no-cache

# Make sure run.sh is executable
RUN chmod +x run.sh

# 6. Expose the port (Render auto-detects $PORT)
EXPOSE 8000

# 7. Run with Gunicorn + Uvicorn workers
CMD ["./run.sh"]