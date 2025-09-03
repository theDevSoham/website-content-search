from fastapi import Request
from app.services.weaviate_service import WeaviateService

def get_weaviate(req: Request) -> WeaviateService:
    return req.app.state.weaviate