from fastapi import FastAPI
from app.api.routers import router as api_router
from app.core.config import Settings

settings = Settings()

app = FastAPI(
    title="HTML Search API",
    description="Backend for HTML DOM Content Search",
    version="0.1.0"
)

# Attach to app.state
app.state.settings = settings

# Include API routes
app.include_router(api_router, prefix="/api")
