import pytest
import time
from app.services.document_processor import DocumentProcessor
from app.services.grading_service import GradingService
from app.models.grading import GradingCriteria

@pytest.mark.benchmark
class TestPerformance:
    async def test_document_processing_speed(self):
        """ทดสอบความเร็วในการประมวลผลเอกสาร"""
        doc_processor = DocumentProcessor()
        content = "Test content " * 1000  # สร้างเนื้อหาขนาดใหญ่
        
        start_time = time.time()
        result = await doc_processor.process_document(
            content,
            {"test": True}
        )
        duration = time.time() - start_time
        
        assert duration < 5.0  # ต้องใช้เวลาน้อยกว่า 5 วินาที
        
    async def test_grading_performance(self):
        """ทดสอบประสิทธิภาพการให้คะแนน"""
        grading_service = GradingService()
        criteria = [
            GradingCriteria(
                name="Test",
                description="Test criteria",
                max_score=10.0
            )
        ]
        
        start_time = time.time()
        result = await grading_service.grade_answer(
            reference_answer="Reference " * 100,
            student_answer="Student " * 100,
            criteria=criteria
        )
        duration = time.time() - start_time
        
        assert duration < 30.0  # ต้องใช้เวลาน้อยกว่า 30 วินาที