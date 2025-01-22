import pytest
from app.services.document_processor import DocumentProcessor
from app.services.grading_service import GradingService
from app.models.document import DocumentCreate
from app.models.grading import GradingCriteria

@pytest.mark.integration
class TestGradingPipeline:
    async def test_complete_grading_flow(self):
        """ทดสอบกระบวนการตรวจให้คะแนนทั้งหมด"""
        # สร้างเอกสารตัวอย่าง
        reference_doc = DocumentCreate(
            title="Reference Answer",
            content="This is a reference answer",
            document_type="reference",
            class_id=1,
            assignment_id=1,
            created_by=1
        )
        
        student_doc = DocumentCreate(
            title="Student Answer",
            content="This is a student answer",
            document_type="answer",
            class_id=1,
            assignment_id=1,
            created_by=2
        )
        
        # สร้างเกณฑ์การให้คะแนน
        criteria = [
            GradingCriteria(
                name="Content",
                description="Content accuracy",
                max_score=10.0
            )
        ]
        
        # ทดสอบขั้นตอนทั้งหมด
        try:
            # 1. Process documents
            doc_processor = DocumentProcessor()
            ref_result = await doc_processor.process_and_embed_documents(
                reference_doc.content,
                {"doc_type": "reference"}
            )
            student_result = await doc_processor.process_and_embed_documents(
                student_doc.content,
                {"doc_type": "answer"}
            )
            
            # 2. Grade answer
            grading_service = GradingService()
            result = await grading_service.grade_answer(
                reference_answer=reference_doc.content,
                student_answer=student_doc.content,
                criteria=criteria
            )
            
            # ตรวจสอบผลลัพธ์
            assert ref_result['success']
            assert student_result['success']
            assert result.total_score >= 0
            assert result.feedback
            
        except Exception as e:
            pytest.fail(f"Integration test failed: {str(e)}")