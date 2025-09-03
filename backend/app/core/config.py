# app/core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    WEAVIATE_URL: str
    WEAVIATE_API_KEY: str
    WEAVIATE_COLLECTION: str
    HUGGINGFACE_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
        
    model_config = SettingsConfigDict(
		env_file=".env",
        extra="ignore", 
	)
        
@lru_cache
def get_settings() -> Settings:
    return Settings()
