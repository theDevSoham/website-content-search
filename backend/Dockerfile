# 1. Base image
FROM python:3.11-slim

# 2. Install uv
RUN pip install --no-cache-dir uv

# 3. Set work directory
WORKDIR /app

# 4. Copy dependency files
COPY pyproject.toml uv.lock* ./

# 5. Install dependencies with uv
RUN uv pip install --system --no-cache .

# 6. Copy the app code
COPY . .

# 7. Expose port
EXPOSE 10000

# 8. Run with Gunicorn + Uvicorn workers
CMD ["uv","run","gunicorn","-k","uvicorn.workers.UvicornWorker","app.main:app","--bind","0.0.0.0:${PORT:-8000}","--workers","4","--reload"]
