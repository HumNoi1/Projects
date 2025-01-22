import pytest
from app.services.grading_service import GradingService
from app.models.grading import GradingCriteria, GradingResult
from unittest.mock import patch, MagicMock

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
            description="ความถูกต้องของคำตอบ",
            max_score=10.0,
            weight=1.0
        ),
        GradingCriteria(
            name="Clarity",
            description="ความชัดเจนในการอธิบาย",
            max_score=5.0,
            weight=0.5
        )
    ]

class TestGradingService:
    @pytest.mark.asyncio
    async def test_create_grading_prompt(
        self,
        grading_service,
        sample_criteria
    ):
        """ทดสอบการสร้าง prompt สำหรับการตรวจให้คะแนน"""
        prompt = await grading_service.create_grading_prompt(
            criteria=sample_criteria,
            reference_answer="นี่คือคำตอบอ้างอิง",
            student_answer="นี่คือคำตอบของนักเรียน",
            language="th"
        )
        
        # ตรวจสอบว่า prompt มีส่วนประกอบที่สำคัญครบถ้วน
        assert "คำตอบอ้างอิง" in prompt
        assert "คำตอบของนักเรียน" in prompt
        assert "Accuracy" in prompt
        assert "Clarity" in prompt
        assert "ความถูกต้องของคำตอบ" in prompt
        assert "ความชัดเจนในการอธิบาย" in prompt

    @pytest.mark.asyncio
    @patch('app.services.llm_service.LLMService')
    async def test_grade_answer(
        self,
        mock_llm_service,
        grading_service,
        sample_criteria
    ):
        """ทดสอบกระบวนการให้คะแนนคำตอบ"""
        # จำลองการตอบกลับจาก LLM
        mock_response = {
            "content": '''{
                "criteria_scores": {
                    "Accuracy": 8.5,
                    "Clarity": 4.0
                },
                "total_score": 12.5,
                "feedback": "คำตอบมีความเข้าใจพื้นฐานที่ดี",
                "confidence_score": 0.85
            }'''
        }
        
        # กำหนดค่าการตอบกลับของ mock
        mock_llm_instance = MagicMock()
        mock_llm_instance.generate_response.return_value = mock_response
        mock_llm_service.return_value = mock_llm_instance
        
        # ทดสอบการให้คะแนน
        result = await grading_service.grade_answer(
            reference_answer="คำตอบอ้างอิง",
            student_answer="คำตอบนักเรียน",
            criteria=sample_criteria,
            language="th"
        )
        
        # ตรวจสอบผลลัพธ์
        assert isinstance(result, GradingResult)
        assert result.total_score == 12.5
        assert "Accuracy" in result.criteria_scores
        assert result.criteria_scores["Accuracy"] == 8.5
        assert result.confidence_score == 0.85