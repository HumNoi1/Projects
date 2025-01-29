from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: int = 19530
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auto Grading System"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()