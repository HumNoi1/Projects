from langchain.embeddings.openai import OpenAIEmbeddings
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        # ใช้ OpenAIEmbeddings แต่เปลี่ยน base URL ไปที่ LMStudio
        self.model = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_base=settings.LMSTUDIO_URL,
            openai_api_key="not-needed",  # LMStudio มักไม่ต้องการ API key
            dimensions=settings.EMBEDDING_DIMENSION,
        )
    
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