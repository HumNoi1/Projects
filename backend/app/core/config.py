from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Existing settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auto Grading System"
    
    # LM Studio Configuration
    LMSTUDIO_API_BASE: str = "http://localhost:1234/v1"
    LLM_TEMPERATURE: float = 0.7
    LLM_TOP_P: float = 0.95
    LLM_MAX_TOKENS: int = 2048
    
    # Milvus Configuration
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: int = 19530
    
    # Supabase Configuration (for testing)
    SUPABASE_URL: str = "https://test.supabase.co"
    SUPABASE_KEY: str = "test-key"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()