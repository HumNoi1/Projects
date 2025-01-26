from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auto Grading System"
    
    LLM_N_GPU_LAYERS: int = 24
    LLM_MODEL_TYPE: str = "llama"
    # Milvus Configuration
    MILVUS_HOST: Optional[str] = "localhost"
    MILVUS_PORT: Optional[int] = 19530
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()