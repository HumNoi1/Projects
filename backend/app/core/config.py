from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auto Grading System"
    
    # Milvus Configuration
    MILVUS_HOST: str
    MILVUS_PORT: int
    
    # Supabase Configuration (จะเพิ่มภายหลัง)
    
    class Config:
        env_file = ".env"

settings = Settings()