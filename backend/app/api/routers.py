from fastapi import APIRouter, Depends
from app.models.request_models import SearchRequest
from app.utils.html_utils import fetch_html
from app.services.chunking_service import EmbeddingsService
from app.deps import get_weaviate

embeddings_service = EmbeddingsService()

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

# handle preflight request
@router.options("/search")
async def options_search():
    """Handle CORS preflight for /search"""
    return {}

@router.post("/search")
async def search(
    request: SearchRequest, 
    weav=Depends(get_weaviate)
):
    
    # 1) Fetch + chunk
    text = fetch_html(request.url)
    chunks, token_counts = embeddings_service.chunk_text(text, return_token_counts=True)
    
    # 2) Embed chunks + upsert
    chunk_embeddings = embeddings_service.embed_texts(chunks)
    weav.upsert_chunks(request.url, chunks, chunk_embeddings, token_counts=token_counts)
    
    # 3) Embed query + search
    query_vec = embeddings_service.embed_texts([request.query])[0]
    results = weav.search_near_vector(query_vec, limit=10, target_url=request.url)
    
    return {
        "ingested_chunks": len(chunks),
        "results": results,
    }
