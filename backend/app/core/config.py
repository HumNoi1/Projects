from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auto Grading System"
    
    # Milvus Configuration
    MILVUS_HOST: str
    MILVUS_PORT: int
    
    # LLM Configuration
    LLM_MODEL_PATH: str = str(Path("models") / "Llama-3.2-3B-Instruct-Q4_K_M.gguf")
    LLM_N_CTX: int = 4096     # context window size
    LLM_N_BATCH: int = 512    # batch size for processing
    LLM_N_THREADS: int = 4    # CPU threads to use
    LLM_N_GPU_LAYERS: int = 32  # GPU layers (ถ้ามี GPU)

    class Config:
        env_file = ".env"

settings = Settings()