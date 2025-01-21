from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auto Grading System"
    
    # Milvus Configuration
    MILVUS_HOST: str
    MILVUS_PORT: int
    
    # llama model path
    LLM_MODEL_PATH: str = "models/llama-3.2-typhoon2-3b-instruct-q4_k_m.gguf"
    LLM_N_CTX: int = 4096
    LLM_N_BATCH: int = 512
    LLM_N_THREADS: int = 4
    LLM_N_GPU_LAYERS: int = 32
    class Config:
        env_file = ".env"

settings = Settings()