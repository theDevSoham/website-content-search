# app/core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    WEAVIATE_URL: str
    HUGGINGFACE_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"   # 👈 tells Pydantic to load from .env file
        
@lru_cache
def get_settings() -> Settings:
    return Settings()
