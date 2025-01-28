import pytest
from datetime import datetime
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.grading_service import GradingService
from app.services.llm_service import LLMService
from app.services.document_processor import DocumentProcessor
from app.models.grading import (
    GradingCriteria,
    GradingResult,
    GradingStatusEnum
)

# ในการทดสอบ เราจำเป็นต้องสร้างข้อมูลตัวอย่างที่สมจริง
# เพื่อให้การทดสอบมีความหมายและครอบคลุมกรณีการใช้งานจริง
@pytest.fixture
def complex_criteria():
    """
    สร้างเกณฑ์การให้คะแนนที่ซับซ้อนเพื่อทดสอบการคำนวณคะแนน
    ประกอบด้วยหลายเกณฑ์ที่มีน้ำหนักต่างกัน
    """
    return [
        GradingCriteria(
            name="ความถูกต้องของเนื้อหา",
            description="ประเมินความถูกต้องของแนวคิดและหลักการ",
            max_score=10.0,
            weight=0.4
        ),
        GradingCriteria(
            name="การวิเคราะห์",
            description="ประเมินความสามารถในการวิเคราะห์และเชื่อมโยง",
            max_score=10.0,
            weight=0.3
        ),
        GradingCriteria(
            name="การสื่อสาร",
            description="ประเมินความชัดเจนในการอธิบายและการใช้ภาษา",
            max_score=10.0,
            weight=0.3
        )
    ]

@pytest.fixture
def mock_grading_result():
    """
    สร้างผลการตรวจที่สมบูรณ์เพื่อใช้ในการทดสอบ
    """
    return GradingResult(
        total_score=8.5,
        criteria_scores={
            "ความถูกต้องของเนื้อหา": 9.0,
            "การวิเคราะห์": 8.0,
            "การสื่อสาร": 8.5
        },
        feedback="คำตอบแสดงความเข้าใจที่ดี มีการวิเคราะห์ที่เป็นระบบ",
        confidence_score=0.95,
        grading_time=datetime.now(),
        evaluator_id="test-model"
    )

class TestGradingService:
    """
    ทดสอบการทำงานของ Grading Service โดยครอบคลุมทั้งการทำงานปกติ
    และการจัดการกับข้อผิดพลาดที่อาจเกิดขึ้น
    """

    @pytest.mark.asyncio
    async def test_prepare_content_success(self):
        """
        ทดสอบการเตรียมเนื้อหาสำหรับการตรวจ
        
        การทดสอบนี้ตรวจสอบว่า:
        1. เนื้อหาที่ยาวเกินถูกตัดให้สั้นลงตามที่กำหนด
        2. มีข้อความแจ้งเตือนการตัดเนื้อหาที่เหมาะสม
        3. ยังคงรักษาเนื้อหาทั้งส่วนต้นและท้ายไว้
        """
        grading_service = GradingService()
        long_content = "test content " * 1000  # สร้างเนื้อหาที่ยาวมาก
        max_length = 1000

        processed_content = await grading_service.prepare_content_for_grading(
            long_content,
            max_length=max_length
        )

        # ตรวจสอบความยาวของเนื้อหา
        assert len(processed_content) <= max_length, (
            f"เนื้อหาควรมีความยาวไม่เกิน {max_length} ตัวอักษร "
            f"แต่มีความยาว {len(processed_content)} ตัวอักษร"
        )

        # ตรวจสอบข้อความแจ้งการตัดเนื้อหา
        truncate_message = "...[เนื้อหาถูกตัดให้สั้นลง]..."
        assert truncate_message in processed_content, (
            "ไม่พบข้อความแจ้งการตัดเนื้อหา"
        )

        # ตรวจสอบว่ายังมีเนื้อหาทั้งส่วนต้นและท้าย
        assert processed_content.startswith("test content"), (
            "ควรคงเนื้อหาส่วนต้นไว้"
        )
        assert processed_content.endswith("test content"), (
            "ควรคงเนื้อหาส่วนท้ายไว้"
        )

    @pytest.mark.asyncio
    async def test_grade_answer_complete_flow(
        self,
        complex_criteria,
        mock_grading_result
    ):
        """
        ทดสอบกระบวนการตรวจให้คะแนนทั้งหมด
        ตั้งแต่การเตรียมเนื้อหาไปจนถึงการได้ผลลัพธ์
        """
        grading_service = GradingService()
        
        # Mock การทำงานของ LLM Service
        with patch.object(
            LLMService,
            'grade_answer',
            new_callable=AsyncMock
        ) as mock_llm_grade:
            mock_llm_grade.return_value = mock_grading_result
            
            result = await grading_service.grade_answer(
                reference_answer="This is a reference answer",
                student_answer="This is a student answer",
                criteria=complex_criteria
            )
            
            # ตรวจสอบผลลัพธ์
            assert isinstance(result, GradingResult)
            assert result.total_score == 8.5
            assert len(result.criteria_scores) == len(complex_criteria)
            assert result.confidence_score >= 0.9

    @pytest.mark.asyncio
    async def test_retry_on_failure(self, complex_criteria, mock_grading_result):
        """ทดสอบระบบ retry เมื่อการตรวจครั้งแรกล้มเหลว"""
        grading_service = GradingService()
        
        # สร้าง mock result ที่ถูกต้อง
        valid_result = GradingResult(
            total_score=9.0,
            criteria_scores={c.name: 9.0 for c in complex_criteria},
            feedback="ผลงานแสดงให้เห็นถึงความเข้าใจที่ดีมาก",  # เพิ่มความยาว feedback
            confidence_score=0.95,
            grading_time=datetime.now(),
            evaluator_id="test-model"
        )
        
        with patch.object(
            LLMService,
            'grade_answer',
            new_callable=AsyncMock
        ) as mock_llm_grade:
            mock_llm_grade.side_effect = [
                Exception("First attempt failed"),
                valid_result  # ใช้ valid_result ที่สร้างขึ้น
            ]
            
            result = await grading_service.grade_answer(
                reference_answer="Reference",
                student_answer="Student",
                criteria=complex_criteria,
                retries=1
            )
            
            assert isinstance(result, GradingResult)
            assert mock_llm_grade.call_count == 2

    @pytest.mark.asyncio
    async def test_validate_grading_result(self, complex_criteria):
        """ทดสอบการตรวจสอบความถูกต้องของผลการให้คะแนน"""
        grading_service = GradingService()
        
        # สร้างผลลัพธ์ที่ถูกต้อง
        valid_result = GradingResult(
            total_score=9.0,
            criteria_scores={
                criterion.name: 9.0 for criterion in complex_criteria
            },
            feedback="คำตอบแสดงความเข้าใจที่ดีและมีการอธิบายที่ชัดเจน",  # เพิ่มความยาว feedback
            confidence_score=0.95,
            grading_time=datetime.now(),
            evaluator_id="test-model"
        )
        
        assert await grading_service.validate_grading_result(
            valid_result,
            complex_criteria
        )
        
        # ทดสอบผลลัพธ์ที่ไม่ถูกต้อง (คะแนนเกินพิกัด)
        invalid_result = GradingResult(
            total_score=11.0,  # เกินคะแนนเต็ม
            criteria_scores={
                criterion.name: 11.0 for criterion in complex_criteria
            },
            feedback="Invalid score",
            confidence_score=0.95,
            grading_time=datetime.now(),
            evaluator_id="test-model"
        )
        
        assert not await grading_service.validate_grading_result(
            invalid_result,
            complex_criteria
        )

    @pytest.mark.asyncio
    async def test_evaluate_grading_confidence(self, mock_grading_result):
        """
        ทดสอบการประเมินความมั่นใจในผลการตรวจ
        """
        grading_service = GradingService()
        
        # ทดสอบกรณีความมั่นใจสูง
        assert await grading_service.evaluate_grading_confidence(
            mock_grading_result,
            threshold=0.9
        )
        
        # ทดสอบกรณีความมั่นใจต่ำ
        low_confidence_result = mock_grading_result.copy()
        low_confidence_result.confidence_score = 0.5
        
        assert not await grading_service.evaluate_grading_confidence(
            low_confidence_result,
            threshold=0.9
        )