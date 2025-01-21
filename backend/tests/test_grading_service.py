import pytest
from app.services.grading_service import GradingService
from app.models.grading import GradingCriteria, GradingResult
from unittest.mock import patch

@pytest.fixture
def grading_service():
    """สร้าง GradingService instance สำหรับการทดสอบ"""
    return GradingService()

@pytest.fixture
def sample_criteria():
    """สร้างเกณฑ์การให้คะแนนตัวอย่าง"""
    return [
        GradingCriteria(
            name="Accuracy",
            description="Correctness of the answer",
            max_score=10.0,
            weight=1.0
        ),
        GradingCriteria(
            name="Clarity",
            description="Clarity of explanation",
            max_score=5.0,
            weight=0.5
        )
    ]

class TestGradingService:
    async def test_create_grading_prompt(
        self,
        grading_service,
        sample_criteria
    ):
        """ทดสอบการสร้าง prompt สำหรับการตรวจให้คะแนน"""
        prompt = await grading_service.create_grading_prompt(
            criteria=sample_criteria,
            reference_answer="Reference answer",
            student_answer="Student answer",
            language="th"
        )
        
        assert "Reference answer" in prompt
        assert "Student answer" in prompt
        assert "Accuracy" in prompt
        assert "Clarity" in prompt

    @patch('app.services.llm_service.LLMService')
    async def test_grade_answer(
        self,
        mock_llm_service,
        grading_service,
        sample_criteria
    ):
        """ทดสอบการให้คะแนนคำตอบ"""
        # Mock LLM response
        mock_response = {
            "content": '''{
                "criteria_scores": {
                    "Accuracy": 8.5,
                    "Clarity": 4.0
                },
                "total_score": 12.5,
                "feedback": "Good answer",
                "confidence_score": 0.85
            }'''
        }
        mock_llm_service.generate_response.return_value = mock_response
        
        result = await grading_service.grade_answer(
            reference_answer="Reference",
            student_answer="Student",
            criteria=sample_criteria
        )
        
        assert isinstance(result, GradingResult)
        assert result.total_score == 12.5
        assert "Accuracy" in result.criteria_scores
        assert result.confidence_score > 0