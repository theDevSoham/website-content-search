# Website Content Search

This project provides a **FastAPI backend** and **React + Tailwind frontend** that fetches and parses website content, chunks the text, generates embeddings with HuggingFace, and stores/searches them in a **Weaviate vector database**.

It is designed for experimentation with RAG-like search systems using arbitrary websites as input.

---

## 🚀 Features

* **FastAPI** backend with clean routing and dependency injection.
* **Embeddings service** using HuggingFace transformers.
* **Weaviate service** for vector storage and semantic search.
* **React + Tailwind** frontend SPA for user interaction.
* **Dockerized** deployment with Gunicorn + Uvicorn workers.
* Configurable via `.env` file.

---

## 📦 Prerequisites

* [Python 3.10+](https://www.python.org/downloads/)
* [uv](https://docs.astral.sh/uv/) (for backend package management)
* [Node.js 18+](https://nodejs.org/en/download/) (for frontend)
* [Docker](https://docs.docker.com/get-docker/) and Docker Compose (optional, for containerized deployment)
* A running **Weaviate instance** (local or cloud).

---

## ⚙️ Configuration

Create a `.env` file in the **backend** root:

```ini
# FastAPI settings
PROJECT_NAME=Website Content Search
PROJECT_VERSION=0.1.0
HUGGINGFACE_MODEL=<transformer model>

# Weaviate settings
WEAVIATE_URL=<weaviate instance rest url>
WEAVIATE_API_KEY=<api key>
WEAVIATE_COLLECTION=<Collection name>
```

Create a `.env.local` file in the **frontend** root:

```ini
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## 🛠️ Backend: Local Development Setup

### 1. Clone repository

```bash
git clone https://github.com/theDevSoham/website-content-search.git
cd website-content-search/backend
```

### 2. Install dependencies with uv

```bash
uv sync
```

### 3. Run the server (hot reload)

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 💻 Frontend: Local Development Setup

### 1. Navigate to frontend

```bash
cd website-content-search/frontend
```

### 2. Install dependencies

```bash
npm install
# or
yarn install
```

### 3. Run development server

```bash
npm run dev
# or
yarn dev
```

The app will be available at [http://localhost:5173](http://localhost:5173).

---

## 🐳 Docker Deployment

### Build backend image

```bash
cd backend
docker build -t website-content-search .
```

### Run backend container

```bash
docker run -p 8000:8000 --env-file .env website-content-search
```

For frontend, you can build a production-ready static site and serve it with Nginx:

```bash
cd frontend
npm run build
```

---

## ⚡ Gunicorn + Uvicorn Setup (Backend)

Inside Docker, the app runs with Gunicorn (process manager) and Uvicorn workers:

```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --workers 4
```

This ensures:

* Multiple workers for concurrency
* Proper process management (unlike bare Uvicorn)

---

## 🔎 Example API Usage

### POST `/api/search`

#### Request body:

```json
{
  "url": "https://justfuckingusehtml.com/",
  "query": "What is the main message?"
}
```

#### Response:

```json
{
  "ingested_chunks": 12,
  "results": "results": [
		...
        {
            "uuid": "b2961672-8d8a-56ff-85d8-d0fbc94b9764",
            "url": "https://justfuckingusehtml.com/",
            "chunk_index": 6,
            "tokens": 500,
            "content": "s the kind of page that makes you want to write a love letter to html ...",
            "distance": 0.5218571424484253
        },
        {
            "uuid": "29b17d12-6edf-5b86-af8a-a18acf98d713",
            "url": "https://justfuckingusehtml.com/",
            "chunk_index": 2,
            "tokens": 500,
            "content": "##tion error \". get the fuck outta here. and \" tree shaking \"? ...",
            "distance": 0.5922361612319946
        },
		...
  ]
}
```

---

## 🗄️ Weaviate Setup

### Option 1: Cloud (recommended)

* Sign up at [Weaviate Cloud Service (WCS)](https://console.weaviate.cloud/).
* Create a cluster and copy the endpoint + API key into `.env`.

### Option 2: Local Docker

Run a local Weaviate instance:

```bash
docker run -d \
  -p 8080:8080 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  semitechnologies/weaviate:latest
```

Update `.env` with:

```
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=
```

---

## 📚 Tech Stack

* **FastAPI** (backend framework)
* **HuggingFace Transformers** (text embeddings)
* **Weaviate** (vector database)
* **React + Tailwind** (frontend SPA)
* **Gunicorn + Uvicorn** (production server)
* **Docker** (containerization)

---

## 🧪 Development Notes

* Hot reload is supported with `uv run uvicorn --reload`.
* Frontend uses Vite for fast development.
* Use Docker for production deployment (ensures Gunicorn workers & clean shutdowns).
* Large HTML pages are tokenized into 500–512 token chunks to fit HuggingFace model constraints.

---

## ✅ Next Steps

* Add authentication (optional).
* Support multiple embedding models.
* Implement relevance scoring & reranking.
* Deploy frontend + backend together via Docker Compose.

---
