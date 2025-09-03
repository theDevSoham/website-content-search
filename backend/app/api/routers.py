from fastapi import APIRouter, Depends
from app.models.request_models import SearchRequest
from app.utils.html_utils import fetch_html
from app.services.chunking_service import EmbeddingsService

embeddings_service = EmbeddingsService()

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/search")
async def search(request: SearchRequest):
    # Step 1: Fetch HTML
    text = fetch_html(request.url)
    
    # Step 2: Chunk text
    chunks = embeddings_service.chunk_text(text)
    print("Chunks: \n")
    print(chunks)
    
    # Step 3: Embed chunks
    embeddings = embeddings_service.embed_texts(chunks)
    print("Embeddings: \n")
    print(embeddings)
    
    return {
        "url": request.url,
        "query": request.query,
        "chunks_preview": chunks[:2],  # preview first 2 chunks
        "embeddings_dim": len(embeddings[0]),
        "total_chunks": len(chunks),
    }
