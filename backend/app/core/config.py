from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # API configuration
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "Grading LLM"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Supabase
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    
    # LMStudio
    LMSTUDIO_URL: str = "http://localhost:1234/v1"
    LMSTUDIO_MODEL: str = "llama-3.2-3b-instruct"
    
    # Embedding model
    EMBEDDING_MODEL: str ="text-embedding-bge-m3"
    EMBEDDING_DIMENSION: int = 1536
    
    # Milvus
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: int = 19530
    MILVUS_COLLECTION: str = "grading_docs"
    
    # File storage
    UPLOAD_DIR: str = "uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()