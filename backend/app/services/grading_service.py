# app/services/grading_service.py
from typing import Dict, Any, List
from .llm_client import LMStudioLLMClient
from .embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)

class GradingServiceError(Exception):
    """Custom exception สำหรับ GradingService"""
    pass

class GradingService:
    """บริการสำหรับการตรวจงานโดยใช้ LLM"""
    
    def __init__(self):
        self.llm_client = LMStudioLLMClient()
        self.embedding_service = EmbeddingService()
        
    def validate_rubric(self, rubric: Dict[str, Any]) -> None:
        """
        ตรวจสอบความถูกต้องของ rubric format
        
        Args:
            rubric: เกณฑ์การให้คะแนนที่ต้องการตรวจสอบ
            
        Raises:
            GradingServiceError: เมื่อ rubric ไม่ถูกต้อง
        """
        if not isinstance(rubric, dict):
            raise GradingServiceError("Rubric must be a dictionary")
            
        required_fields = {'weight', 'criteria'}
        for criterion, details in rubric.items():
            if not isinstance(details, dict):
                raise GradingServiceError(
                    f"Each criterion in rubric must be a dictionary, got {type(details)} for {criterion}"
                )
            
            missing_fields = required_fields - set(details.keys())
            if missing_fields:
                raise GradingServiceError(
                    f"Missing required fields {missing_fields} in criterion '{criterion}'"
                )
            
            if not isinstance(details['weight'], (int, float)):
                raise GradingServiceError(
                    f"Weight must be a number, got {type(details['weight'])} for {criterion}"
                )
            
            if not isinstance(details['criteria'], str):
                raise GradingServiceError(
                    f"Criteria must be a string, got {type(details['criteria'])} for {criterion}"
                )

    async def grade_assignment(
        self,
        student_answer: str,
        reference_answer: str,
        rubric: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        ตรวจงานโดยเปรียบเทียบคำตอบของนักเรียนกับเฉลย
        
        Args:
            student_answer: คำตอบของนักเรียน
            reference_answer: เฉลย
            rubric: เกณฑ์การให้คะแนน
            
        Raises:
            GradingServiceError: เมื่อเกิดข้อผิดพลาดในการตรวจงาน
        """
        # ตรวจสอบ input
        if not student_answer or not reference_answer or not rubric:
            raise GradingServiceError("Missing required input: student_answer, reference_answer, and rubric are required")
            
        # ตรวจสอบ rubric format
        self.validate_rubric(rubric)

        try:
            # สร้าง prompt สำหรับการตรวจ
            system_prompt = """You are an expert grader. 
            Grade the student's answer based on the reference answer and rubric.
            Provide a score and detailed feedback."""
            
            prompt = f"""
            Reference Answer: {reference_answer}
            Student Answer: {student_answer}
            Rubric: {rubric}
            
            Please grade this answer and provide:
            1. Score
            2. Detailed feedback
            3. Areas for improvement
            """
            
            # เรียกใช้ LLM เพื่อตรวจงาน
            grading_result = await self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt
            )
            
            # ตรวจสอบผลลัพธ์จาก LLM
            if "Error" in grading_result:
                raise GradingServiceError(f"LLM error: {grading_result}")
            
            return {
                "success": True,
                "grading_result": grading_result
            }
            
        except Exception as e:
            logger.error(f"Error grading assignment: {str(e)}")
            raise GradingServiceError(f"Failed to grade assignment: {str(e)}")