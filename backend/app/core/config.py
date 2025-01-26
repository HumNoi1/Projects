from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auto Grading System"
    
    # HuggingFace Configuration
    MODEL_NAME: str = "bartowski/Llama-3.2-3B-Instruct-GGUF"  # เปลี่ยนเป็น repo ที่มีไฟล์ GGUF
    MODEL_FILE: str = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"    # ชื่อไฟล์ GGUF
    HUGGINGFACE_TOKEN: Optional[str] = None
    N_GPU_LAYERS: int = -1  # -1 คือใช้ทุก layers
    
    # Milvus Configuration
    MILVUS_HOST: Optional[str] = "localhost"
    MILVUS_PORT: Optional[int] = 19530
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()