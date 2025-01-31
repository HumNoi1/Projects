# tests/test_lmstudio_connection.py
import pytest
from app.services.llm_client import LMStudioLLMClient
from app.services.lmstudio_client import LMStudioClient
import logging

logger = logging.getLogger(__name__)

class TestLMStudioConnection:
    """ทดสอบการเชื่อมต่อกับ LM-Studio ทั้ง LLM และ Embedding"""

    @pytest.fixture
    def llm_client(self):
        return LMStudioLLMClient()

    @pytest.fixture
    def embedding_client(self):
        return LMStudioClient()

    @pytest.mark.asyncio
    async def test_llm_connection(self, llm_client):
        """ทดสอบการเชื่อมต่อกับ LLM"""
        try:
            # ทดสอบด้วย prompt ง่ายๆ
            test_prompt = "Hello, how are you?"
            response = await llm_client.generate(test_prompt)
            
            assert response is not None
            assert isinstance(response, str)
            assert len(response) > 0
            
            logger.info(f"LLM Response: {response}")
            
        except Exception as e:
            logger.error(f"LLM connection test failed: {str(e)}")
            raise

    @pytest.mark.asyncio
    async def test_embedding_connection(self, embedding_client):
        """ทดสอบการเชื่อมต่อกับ Embedding Model"""
        try:
            # ทดสอบสร้าง embedding จากข้อความ
            test_texts = ["This is a test sentence.", "Another test sentence."]
            embeddings = await embedding_client.create_embeddings(test_texts)
            
            assert embeddings is not None
            assert len(embeddings) == 2
            assert len(embeddings[0]) == 1024  # ขนาดของ bge-m3
            
            logger.info(f"Generated embeddings shape: {len(embeddings)}x{len(embeddings[0])}")
            
        except Exception as e:
            logger.error(f"Embedding connection test failed: {str(e)}")
            raise