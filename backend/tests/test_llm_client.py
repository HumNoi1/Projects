# backend/tests/test_llm_client.py
import pytest
import asyncio
from app.services.llm_client import LMStudioLLMClient
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_llm_client_generate():
    # Mock response data
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "This is a test response from LLM"
                }
            }
        ]
    }
    
    # Test with mocked client
    with patch('httpx.AsyncClient') as mock_client:
        # Setup mock
        mock_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_instance
        mock_instance.get.return_value = AsyncMock()
        
        mock_response_obj = AsyncMock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status = AsyncMock()
        mock_instance.post.return_value = mock_response_obj
        
        # Test
        client = LMStudioLLMClient()
        result = await client.generate("Test prompt", "Test system prompt")
        
        # Verify
        assert result == "This is a test response from LLM"
        mock_instance.post.assert_called_once()