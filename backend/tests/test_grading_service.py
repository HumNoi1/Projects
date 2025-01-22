# backend/tests/integration/test_grading_integration.py
import pytest
from app.services.grading_service import GradingService
from app.models.grading import GradingCriteria, GradingResult
import json

@pytest.fixture
def real_grading_service():
    """
    สร้าง GradingService ที่เชื่อมต่อกับ LLM จริง
    การทดสอบนี้จะใช้เวลานานกว่าและต้องการไฟล์โมเดล LLM
    """
    return GradingService()

@pytest.fixture
def sample_physics_criteria():
    """
    สร้างเกณฑ์การให้คะแนนสำหรับคำถามฟิสิกส์
    เกณฑ์นี้ถูกออกแบบให้ครอบคลุมด้านต่างๆ ของการตอบคำถามทางวิทยาศาสตร์
    """
    return [
        GradingCriteria(
            name="ความถูกต้องทางวิชาการ",
            description="ความถูกต้องของหลักการและแนวคิดทางฟิสิกส์",
            max_score=10.0,
            weight=1.0
        ),
        GradingCriteria(
            name="การอธิบายและการให้เหตุผล",
            description="ความชัดเจนและตรรกะในการอธิบายแนวคิด",
            max_score=5.0,
            weight=0.8
        ),
        GradingCriteria(
            name="การใช้ภาษาทางวิทยาศาสตร์",
            description="การใช้คำศัพท์และการสื่อสารทางวิทยาศาสตร์",
            max_score=5.0,
            weight=0.6
        )
    ]

@pytest.mark.integration
class TestGradingIntegration:
    """
    การทดสอบการทำงานร่วมกันของระบบการให้คะแนนกับ LLM จริง
    
    การทดสอบนี้จะใช้เวลามากกว่าและต้องการทรัพยากรจริง แต่จะช่วยยืนยัน
    การทำงานของระบบในสภาพแวดล้อมจริง
    """
    
    @pytest.mark.asyncio
    async def test_grade_physics_answer(
        self,
        real_grading_service,
        sample_physics_criteria
    ):
        """
        ทดสอบการให้คะแนนคำตอบวิชาฟิสิกส์โดยใช้ LLM จริง
        
        ทดสอบนี้จะตรวจสอบว่า LLM สามารถ:
        1. เข้าใจเนื้อหาทางฟิสิกส์
        2. ให้คะแนนตามเกณฑ์ที่กำหนด
        3. ให้ feedback ที่มีความหมายและเป็นประโยชน์
        """
        reference_answer = """
        แรงโน้มถ่วงเป็นแรงดึงดูดระหว่างวัตถุที่มีมวล โดยมีขนาดแปรผันตรงกับผลคูณของมวลทั้งสอง 
        และแปรผกผันกับกำลังสองของระยะทางระหว่างวัตถุ ตามกฎแรงโน้มถ่วงสากลของนิวตัน 
        ในกรณีของโลก แรงโน้มถ่วงทำให้วัตถุตกลงสู่พื้นด้วยความเร่งคงที่ประมาณ 9.8 m/s²
        """
        
        student_answer = """
        แรงโน้มถ่วงคือแรงที่ดึงดูดระหว่างวัตถุสองชิ้น ยิ่งวัตถุมีมวลมาก แรงก็จะมากขึ้น 
        และถ้าวัตถุอยู่ห่างกัน แรงก็จะน้อยลง บนโลกทำให้ของตกลงพื้นด้วยความเร่ง g = 9.8
        """
        
        # ทดสอบการให้คะแนนด้วย LLM จริง
        result = await real_grading_service.grade_answer(
            reference_answer=reference_answer,
            student_answer=student_answer,
            criteria=sample_physics_criteria,
            language="th"
        )
        
        # ตรวจสอบโครงสร้างของผลลัพธ์
        assert isinstance(result, GradingResult)
        assert isinstance(result.total_score, float)
        assert isinstance(result.criteria_scores, dict)
        assert isinstance(result.feedback, str)
        
        # ตรวจสอบความสมเหตุสมผลของคะแนน
        assert 0 <= result.total_score <= sum(c.max_score * c.weight for c in sample_physics_criteria)
        for criterion in sample_physics_criteria:
            assert criterion.name in result.criteria_scores
            assert 0 <= result.criteria_scores[criterion.name] <= criterion.max_score
        
        # ตรวจสอบคุณภาพของ feedback
        assert len(result.feedback) > 50  # feedback ควรมีความยาวพอสมควร
        assert "แรงโน้มถ่วง" in result.feedback.lower()  # ควรมีการอ้างถึงคำสำคัญ
        
        print("\nผลการตรวจ:")
        print(f"คะแนนรวม: {result.total_score}")
        print("คะแนนแต่ละเกณฑ์:")
        for name, score in result.criteria_scores.items():
            print(f"- {name}: {score}")
        print(f"\nFeedback:\n{result.feedback}")

    @pytest.mark.asyncio
    async def test_grade_multiple_answers(
        self,
        real_grading_service,
        sample_physics_criteria
    ):
        """
        ทดสอบการให้คะแนนคำตอบหลายรูปแบบ เพื่อตรวจสอบความสม่ำเสมอของ LLM
        """
        reference_answer = """
        แรงเป็นสิ่งที่ทำให้วัตถุเปลี่ยนแปลงการเคลื่อนที่ ตามกฎข้อที่สองของนิวตัน 
        แรงสุทธิเท่ากับมวลคูณความเร่ง (F = ma) แรงมีทั้งขนาดและทิศทาง จึงเป็นปริมาณเวกเตอร์
        """
        
        test_answers = [
            # คำตอบที่ดี
            """แรงเป็นปริมาณเวกเตอร์ที่ทำให้วัตถุเปลี่ยนสภาพการเคลื่อนที่ 
            ตามกฎข้อ 2 ของนิวตัน แรงสุทธิจะเท่ากับมวลคูณด้วยความเร่ง""",
            
            # คำตอบที่พอใช้
            """แรงทำให้วัตถุเคลื่อนที่ มีสูตร F = ma""",
            
            # คำตอบที่ไม่ดี
            """แรงคือพลังงานที่ทำให้ของเคลื่อนที่ได้"""
        ]
        
        results = []
        for answer in test_answers:
            result = await real_grading_service.grade_answer(
                reference_answer=reference_answer,
                student_answer=answer,
                criteria=sample_physics_criteria,
                language="th"
            )
            results.append(result)
            
        # ตรวจสอบว่าคะแนนสะท้อนคุณภาพของคำตอบ
        assert results[0].total_score > results[1].total_score > results[2].total_score