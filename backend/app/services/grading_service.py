from datetime import datetime
import json
import logging
from typing import List, Dict, Any
from app.models.grading import GradingCriteria, GradingResult  # แก้ไขการ import
from .llm_service import LMStudioService

logger = logging.getLogger(__name__)

class GradingService:
    """
    บริการตรวจให้คะแนนที่ใช้ LLM ในการวิเคราะห์และประเมินคำตอบของนักเรียน
    คลาสนี้จัดการการสร้าง prompt, การประมวลผลคำตอบจาก LLM, และการตรวจสอบความถูกต้องของผลลัพธ์
    """

    def __init__(self):
        """
        เริ่มต้นบริการตรวจให้คะแนนโดยสร้าง instance ของ LLMService
        """
        self.llm_service = LMStudioService()

    async def create_grading_prompt(
        self,
        criteria: List[GradingCriteria],
        reference_answer: str,
        student_answer: str,
        language: str = "th"
    ) -> str:
        """
        สร้าง prompt ที่ชัดเจนสำหรับ LLM เพื่อให้ได้ผลลัพธ์ในรูปแบบ JSON ที่ถูกต้อง
        """
        criteria_text = "\n".join([
            f"- {c.name} (คะแนนเต็ม: {c.max_score}, น้ำหนัก {c.weight}):\n {c.description}"
            for c in criteria
        ])
        
        # ปรับปรุง prompt ให้เน้นย้ำเรื่องรูปแบบ JSON
        prompt = f"""คูณเป็นผู้เชี่ยวชาญในการตรวจข้อสอบ ให้ตรวจและให้คะแนนตามเกณฑ์ที่กำหนด
        
        เกณฑ์การให้คะแนน:
        {criteria_text}
        
        คำตอบอ้างอิง:
        {reference_answer}
        
        คำตอบของนักเรียน:
        {student_answer}
        
        คำแนะนำสำคัญ:
        1. กรุณาตรวจให้คะแนนเพียงครั้งเดียว
        2. ตอบกลับมาในรูปแบบ JSON หนึ่งชุดเท่านั้น
        3. ห้ามมีข้อความอื่นใดนอกเหนือจาก JSON
        4. ใช้รูปแบบด้านล่างนี้อย่างเคร่งครัด:
        
        {{
            "criteria_scores": {{
                "<ชื่อเกณฑ์>": <คะแนน(ตัวเลข)>,
            }},
            "total_score": <คะแนนรวม(ตัวเลข)>,
            "feedback": "<คำแนะนำเป็นภาษา{language}>",
            "confidence_score": <ความมั่นใจ(0-1)>
        }}
        """
        
        return prompt

    async def validate_grading_result(
        self,
        result: GradingResult,
        criteria: List[GradingCriteria]
    ) -> bool:
        """
        ตรวจสอบความถูกต้องของผลการให้คะแนน
        
        Args:
            result: ผลการให้คะแนนที่ได้จาก LLM
            criteria: เกณฑ์การให้คะแนนที่ใช้
            
        Returns:
            True ถ้าผลลัพธ์ถูกต้อง, False ถ้าไม่ถูกต้อง
        """
        try:
            # ตรวจสอบว่ามีคะแนนครบทุกเกณฑ์
            expected_criteria = {c.name for c in criteria}
            if set(result.criteria_scores.keys()) != expected_criteria:
                logger.error("Missing criteria scores")
                return False
            
            # ตรวจสอบช่วงคะแนนรวม
            max_total = sum(c.max_score * c.weight for c in criteria)
            if not (0 <= result.total_score <= max_total):
                logger.error(f"Total score {result.total_score} out of range [0, {max_total}]")
                return False
            
            # ตรวจสอบคะแนนแต่ละเกณฑ์
            for criterion in criteria:
                score = result.criteria_scores.get(criterion.name, 0)
                if not (0 <= score <= criterion.max_score):
                    logger.error(f"Score for {criterion.name} out of range [0, {criterion.max_score}]")
                    return False
            
            # ตรวจสอบ confidence score
            if not (0 <= result.confidence_score <= 1):
                logger.error(f"Confidence score {result.confidence_score} out of range [0, 1]")
                return False
            
            return True

        except Exception as e:
            logger.error(f"Error validating grading result: {str(e)}")
            return False

    async def grade_answer(
        self,
        reference_answer: str,
        student_answer: str,
        criteria: List[GradingCriteria],
        language: str = "th"
    ) -> GradingResult:
        try:
            criteria_dicts = [c.model_dump() for c in criteria]
            
            prompt = self.llm_service.create_grading_prompt(
                reference_answer=reference_answer,
                student_answer=student_answer,
                criteria=criteria_dicts,
                language=language
            )
            
            response_text = await self.llm_service.generate_completion(prompt)
            
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                logger.error("Invalid JSON response from LLM")
            
            return GradingResult(
                **result,
                grading_time=datetime.now(),
                evaluator_id="lm-studio-grader"
            )
        
        except Exception as e:
            logger.error(f"Error grading answer: {str(e)}")
            raise

    
    def _validate_grading_data(self, data: Dict) -> None:
        """ตรวจสอบความถูกต้องของข้อมูลทีการให้คะแนน"""
        required_fields = {'criteria_scores', 'total_score', 'feedback', 'confidence_score'}
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # ตรวจสอบประเภทของข้อมูล
        if not isinstance(data['criteria_scores'], dict):
            raise ValueError("criteria_scores must be an object")
        if not isinstance(data['total_score'], (int, float)):
            raise ValueError("total_score must be a number")
        if not isinstance(data['feedback'], str):
            raise ValueError("feedback must be a string")
        if not isinstance(data['confidence_score'], (int, float)):
            raise ValueError("confidence_score must be a number")