from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    app_name: str = "Nexus AI"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "production"
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    openai_max_tokens: int = 4096
    
    huggingface_api_key: str = ""
    huggingface_model: str = "google/flan-t5-large"
    llm_provider: str = "openai"
    
    frontend_url: str = "https://nexus-ai.vercel.app"
    backend_url: str = "https://nexus-ai-backend.onrender.com"
    
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://nexus-ai.vercel.app",
        "https://*.vercel.app",
    ]
    
    log_level: str = "INFO"
    max_retries: int = 5
    sandbox_timeout: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()