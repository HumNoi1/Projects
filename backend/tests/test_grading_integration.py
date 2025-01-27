# tests/test_grading_integration.py
import pytest
from app.models.grading import GradingCriteria  # ใช้ import แบบนี้แทน
from app.services.grading_service import GradingService

@pytest.fixture
def sample_criteria():
    """สร้างเกณฑ์การให้คะแนนตัวอย่าง"""
    return [
        GradingCriteria(
            name="ความถูกต้อง",
            description="ความถูกต้องของเนื้อหา",
            max_score=10.0,
            weight=1.0
        ),
        GradingCriteria(
            name="การอธิบาย",
            description="ความชัดเจนในการอธิบาย",
            max_score=5.0,
            weight=0.8
        )
    ]

@pytest.mark.asyncio
async def test_grade_answer(sample_criteria):
    """ทดสอบการตรวจให้คะแนน"""
    service = GradingService()
    
    reference = "การเคลื่อนที่แนวตรงคือการเคลื่อนที่ในแนวเส้นตรง มีความเร็วและความเร่งในทิศทางเดียวกัน"
    student = "การเคลื่อนที่แนวตรงคือการเคลื่อนที่ในแนวเส้นตรง"
    
    result = await service.grade_answer(
        reference_answer=reference,
        student_answer=student,
        criteria=sample_criteria
    )
    
    assert result.total_score >= 0
    assert result.total_score <= sum(c.max_score * c.weight for c in sample_criteria)
    assert len(result.feedback) > 0