from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from app.core.config import settings
import os

class BackupEmbeddingService:
    """
    คลาสสำรองในกรณีที่ LMStudio ไม่รองรับ embeddings API
    """
    def __init__(self):
        try:
            # พยายามใช้ OpenAI-compatible API ก่อน
            self.model = OpenAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                openai_api_base=settings.LMSTUDIO_URL,
                openai_api_key="not-needed",
                dimensions=settings.EMBEDDING_DIMENSION,
            )
            # ทดสอบว่าใช้งานได้หรือไม่
            self.model.embed_query("test")
            self.using_lmstudio = True
        except Exception as e:
            print(f"Warning: Could not use LMStudio for embeddings: {e}")
            print("Falling back to HuggingFace embeddings")
            # ถ้าไม่สามารถใช้ LMStudio ได้ ให้ใช้ HuggingFace แทน
            self.model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            self.using_lmstudio = False
    
    async def get_embeddings(self, texts):
        """
        สร้าง embeddings สำหรับรายการข้อความ
        """
        if isinstance(texts, str):
            texts = [texts]
            
        embeddings = self.model.embed_documents(texts)
        return embeddings
    
    async def get_query_embedding(self, query):
        """
        สร้าง embedding สำหรับคำถาม
        """
        return self.model.embed_query(query)