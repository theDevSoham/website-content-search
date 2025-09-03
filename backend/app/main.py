from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routers import router as api_router
from app.core.config import Settings
from app.services.weaviate_service import WeaviateService

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")

    app.state.settings = settings
    app.state.weaviate = WeaviateService()

    yield

    print("Application shutdown...")

    if hasattr(app.state, "weaviate"):
        app.state.weaviate.close()

app = FastAPI(
    title="HTML Search API",
    description="Backend for HTML DOM Content Search",
    version="0.1.0",
    lifespan=lifespan
)

# Include API routes
app.include_router(api_router, prefix="/api")
