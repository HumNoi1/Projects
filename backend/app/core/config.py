# app/core/config.py
from http.client import REQUEST_TIMEOUT
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: int = 19530
    
    # LM-Studio Configuration
    LMSTUDIO_API_BASE: str
    EMBEDDING_MODEL_NAME: str  # เพิ่มตัวแปรนี้
    LLM_MODEL_NAME: str
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7
    EMBEDDING_DIMENSION: int = 1024
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auto Grading System"
    
    REQUEST_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()