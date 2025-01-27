# tests/test_lm_studio_service.py
import pytest
from httpx import AsyncClient
from app.services.llm_service import LMStudioService
from app.core.config import settings

@pytest.fixture
async def lm_studio_service():
    """สร้าง LMStudioService สำหรับการทดสอบ"""
    return LMStudioService()

@pytest.mark.asyncio
async def test_lm_studio_connection(lm_studio_service):
    """ทดสอบการเชื่อมต่อกับ LM Studio"""
    async with AsyncClient() as client:
        response = await client.get(f"{settings.LMSTUDIO_API_BASE}/v1/models")
        assert response.status_code == 200
        assert len(response.json()["data"]) > 0

@pytest.mark.asyncio
async def test_generate_completion(lm_studio_service):
    """ทดสอบการสร้าง completion"""
    prompt = "What is 1+1?"
    result = await lm_studio_service.generate_completion(prompt)
    assert isinstance(result, str)
    assert len(result) > 0