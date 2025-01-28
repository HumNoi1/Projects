import asyncio
from unittest import mock
from urllib import response
import pytest
import json
from unittest.mock import patch, AsyncMock
from datetime import datetime
from app.services.llm_service import LLMService
from app.models.grading import GradingCriteria, GradingResult

# Test data fixtures
@pytest.fixture
def sample_criteria():
    """
    Creates a set of sample grading criteria for testing
    """
    return [
        GradingCriteria(
            name="Content Accuracy",
            description="Evaluates the accuracy of the content",
            max_score=10.0,
            weight=0.6
        ),
        GradingCriteria(
            name="Expression",
            description="Evaluates clarity of expression",
            max_score=5.0,
            weight=0.4
        )
    ]

@pytest.fixture
def sample_reference_answer():
    return """
    The process of photosynthesis converts light energy into chemical energy.
    This process occurs in the chloroplasts of plant cells and produces
    glucose and oxygen while consuming carbon dioxide and water.
    """

@pytest.fixture
def sample_student_answer():
    return """
    Photosynthesis changes sunlight into energy that plants can use.
    It happens in chloroplasts and makes sugar and oxygen.
    Plants need carbon dioxide and water for this process.
    """

class TestLLMService:
    """
    Test suite for the LLM Service class
    Tests both the API interaction and response processing
    """

    @pytest.mark.asyncio
    async def test_make_request_success(self):
        """ Tests successful API request"""
        llm_service = LLMService()
        
        # Mock a successful API response
        mock_response = {
            "choices": [{
                "message": {
                    "content": "Test response"
                }
            }]
        }
        
        with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            #setup the mock to return the response
            mock_post.return_value = AsyncMock()
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = AsyncMock()
            
            response = await llm_service._make_request(
                "chat/completions",
                {"messages": [{"role": "user", "content": "Test prompt"}]}
            )
            
            # Wait for any pending coroutines
            if asyncio.iscoroutine(response):
                response = await response
            
            assert response == mock_response
            mock_post.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_response(self):
        """Tests response generation with prompt"""
        llm_service = LLMService()
        test_prompt = "What is 2+2?"
        
        with patch.object(
            llm_service,
            '_make_request',
            new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = {
                "choices": [{
                    "message": {
                        "content": "The answer is 4"
                    }
                }]
            }
            
            response = await llm_service.generate_response(test_prompt)
            assert isinstance(response, str)
            assert "4" in response

    @pytest.mark.asyncio
    async def test_grade_answer_success(
        self,
        sample_criteria,
        sample_reference_answer,
        sample_student_answer
    ):
        """Tests successful grading of a student answer"""
        llm_service = LLMService()
        
        # Mock a valid grading response
        mock_grading_response = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "criteria_scores": {
                            "Content Accuracy": 8.5,
                            "Expression": 4.0
                        },
                        "total_score": 7.1,
                        "feedback": "Good understanding shown",
                        "confidence_score": 0.9
                    })
                }
            }]
        }
        
        with patch.object(
            llm_service,
            '_make_request',
            new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_grading_response
            
            result = await llm_service.grade_answer(
                reference_answer=sample_reference_answer,
                student_answer=sample_student_answer,
                criteria=sample_criteria
            )
            
            assert isinstance(result, GradingResult)
            assert result.total_score == 7.1
            assert len(result.criteria_scores) == 2
            assert result.confidence_score == 0.9

    @pytest.mark.asyncio
    async def test_grade_answer_invalid_response(
        self,
        sample_criteria,
        sample_reference_answer,
        sample_student_answer
    ):
        """Tests handling of invalid LLM response"""
        llm_service = LLMService()
        
        # Mock an invalid response format
        mock_invalid_response = {
            "choices": [{
                "message": {
                    "content": "Invalid JSON response"
                }
            }]
        }
        
        with patch.object(
            llm_service,
            '_make_request',
            new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_invalid_response
            
            with pytest.raises(ValueError):
                await llm_service.grade_answer(
                    reference_answer=sample_reference_answer,
                    student_answer=sample_student_answer,
                    criteria=sample_criteria
                )

    @pytest.mark.asyncio
    async def test_network_error_handling(self):
        """Tests handling of network errors"""
        llm_service = LLMService()
        
        with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = Exception("Network error")
            
            with pytest.raises(Exception) as exc_info:
                await llm_service._make_request(
                    "chat/completions",
                    {"messages": []}
                )
            
            assert "Network error" in str(exc_info.value)