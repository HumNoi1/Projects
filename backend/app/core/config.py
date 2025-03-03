from pydantic_settings import BaseSettings
from typing import List, Optional, Union

class Settings(BaseSettings):
    # API configuration
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "Grading LLM"
    
    # CORS
    CORS_ORIGINS: Union[List[str]] = ["http://localhost:3000"]
    
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
        
    @property
    def cors_origins(self) -> List[str]:
        """ แปลง CORS_ORIGINS เป็นรูปแบบที่ถูกต้องเสมอ """
        if isinstance(self.CORS_ORIGINS, str):
            # ถ้าเป็น string เดียวอาจมีหลาย origins คั่นด้วย comma
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS

settings = Settings()