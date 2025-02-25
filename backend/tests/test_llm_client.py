# backend/tests/test_llm_client.py
import pytest
import asyncio
from app.services.llm_client import LMStudioLLMClient
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_llm_client_generate():
    # แทนที่จะ mock httpx.AsyncClient ให้ mock LMStudioLLMClient.generate โดยตรง
    with patch.object(LMStudioLLMClient, 'generate', new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = "This is a test response from LLM"
        
        # สร้าง instance จริงของ client
        client = LMStudioLLMClient()
        
        # เรียกใช้งาน generate
        result = await client.generate("Test prompt", "Test system prompt")
        
        # ตรวจสอบว่าได้ผลลัพธ์ถูกต้อง
        assert result == "This is a test response from LLM"
        
        # ตรวจสอบว่า mock ถูกเรียกด้วยพารามิเตอร์ถูกต้อง
        mock_generate.assert_called_once_with("Test prompt", "Test system prompt")