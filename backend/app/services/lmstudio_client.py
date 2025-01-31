# app/services/lmstudio_client.py
import httpx
from typing import List
import numpy as np
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class LMStudioClient:
    def __init__(self):
        self.api_base = settings.LMSTUDIO_API_BASE
        self.model = settings.EMBEDDING_MODEL_NAME
        
    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        สร้าง embeddings โดยใช้ LM-Studio API
        
        Args:
            texts: รายการข้อความที่ต้องการสร้าง embeddings
            
        Returns:
            List ของ embedding vectors
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base}/v1/embeddings",
                    json={
                        "model": self.model,
                        "input": texts
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # แปลงผลลัพธ์เป็น list ของ vectors
                embeddings = [item["embedding"] for item in data["data"]]
                return embeddings
                
        except Exception as e:
            logger.error(f"Error creating embeddings with LM-Studio: {str(e)}")
            raise