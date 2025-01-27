# app/core/config.py
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auto Grading System"
    
    # LM Studio Configuration
    LMSTUDIO_API_BASE: str = "http://127.0.0.1:1234"
    
    # Database Configuration
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: int = 19530
    
    # Supabase Configuration - จำเป็นต้องมีค่าเหล่านี้
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Model Configuration
    MODEL_NAME: Optional[str] = "bartowski/Llama-3.2-3B-Instruct-GGUF"
    DEVICE: Optional[str] = "cuda"
    MAX_LENGTH: Optional[int] = 512
    
    # LM Studio Configuration
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.95
    MAX_TOKENS: int = 4096
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"  # อนุญาตให้มี extra fields
    )

settings = Settings()