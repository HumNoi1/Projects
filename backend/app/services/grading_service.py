from datetime import datetime
import logging
from typing import List, Dict, Any, Optional

from app.models.grading import (
    GradingCriteria,
    GradingResult,
    GradingRequest,
    GradingStatusEnum
)
from app.services.llm_service import LLMService
from app.services.document_processor import DocumentProcessor

logger = logging.getLogger(__name__)

class GradingService:
    """
    บริการจัดการการตรวจให้คะแนนที่ทำงานร่วมกับ LLM Service
    
    บริการนี้รับผิดชอบในการ:
    1. ประสานงานระหว่าง Document Processor และ LLM Service
    2. จัดการกระบวนการตรวจให้คะแนน
    3. ตรวจสอบความถูกต้องของผลลัพธ์
    4. จัดการกับข้อผิดพลาดที่อาจเกิดขึ้น
    """

    def __init__(self):
        # สร้าง instances ของ services ที่จำเป็น
        self.llm_service = LLMService()
        self.document_processor = DocumentProcessor()

    async def prepare_content_for_grading(self, content: str, max_length: int = 2000) -> str:
        try:
            # ทำความสะอาดและแบ่งเนื้อหา
            cleaned_content = await self.document_processor.process_document(content)
            processed_content = " ".join(chunk.page_content for chunk in cleaned_content)
            
            if len(processed_content) > max_length:
                # คำนวณความยาวที่จะตัดโดยคำนึงถึงความยาวของข้อความที่จะแทรก
                truncate_message = "\n...[เนื้อหาถูกตัดให้สั้นลง]...\n"
                remaining_length = max_length - len(truncate_message)
                half_length = remaining_length // 2
                
                processed_content = (
                    processed_content[:half_length] +
                    truncate_message +
                    processed_content[-half_length:]
                )
                
            return processed_content
                
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการเตรียมเนื้อหา: {str(e)}")
            raise

    async def grade_answer(
        self,
        reference_answer: str,
        student_answer: str,
        criteria: List[GradingCriteria],
        language: str = "th",
        retries: int = 2
    ) -> GradingResult:
        """
        Grades a student's answer using the specified criteria.
        Includes retry logic and result validation to ensure reliable grading.

        Args:
            reference_answer: The reference answer to grade against
            student_answer: The student's answer to grade
            criteria: List of grading criteria to apply
            language: Preferred language for feedback
            retries: Number of retry attempts for failed grading
            
        Returns:
            A validated GradingResult object
        """
        try:
            # Prepare content for grading
            processed_reference = await self.prepare_content_for_grading(
                reference_answer
            )
            processed_student = await self.prepare_content_for_grading(
                student_answer
            )

            # Attempt grading with retries
            last_error = None
            for attempt in range(retries + 1):
                try:
                    result = await self.llm_service.grade_answer(
                        reference_answer=processed_reference,
                        student_answer=processed_student,
                        criteria=criteria,
                        language=language
                    )

                    # Validate the result
                    if await self.validate_grading_result(result, criteria):
                        return result
                    else:
                        raise ValueError("Invalid grading result format")

                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"Grading attempt {attempt + 1} failed: {str(e)}"
                    )
                    if attempt == retries:
                        raise last_error

            raise last_error

        except Exception as e:
            logger.error(f"Error in grading process: {str(e)}")
            raise

    async def validate_grading_result(
        self,
        result: GradingResult,
        criteria: List[GradingCriteria]
    ) -> bool:
        """
        Performs comprehensive validation of a grading result.
        Checks both format and logical consistency of the grades.

        Args:
            result: The grading result to validate
            criteria: The criteria used for grading
            
        Returns:
            True if the result is valid, False otherwise
        """
        try:
            # Basic structure validation
            if not all(hasattr(result, field) for field in [
                'criteria_scores',
                'total_score',
                'feedback',
                'confidence_score'
            ]):
                logger.error("Missing required fields in grading result")
                return False

            # Validate criteria scores
            for criterion in criteria:
                if criterion.name not in result.criteria_scores:
                    logger.error(f"Missing score for criterion: {criterion.name}")
                    return False

                score = result.criteria_scores[criterion.name]
                if not (0 <= score <= criterion.max_score):
                    logger.error(
                        f"Invalid score range for {criterion.name}: {score}"
                    )
                    return False

            # Validate total score
            max_possible = sum(c.max_score * c.weight for c in criteria)
            if not (0 <= result.total_score <= max_possible):
                logger.error(
                    f"Total score {result.total_score} exceeds maximum possible {max_possible}"
                )
                return False

            # Validate feedback
            if not result.feedback or len(result.feedback.strip()) < 10:
                logger.error("Feedback is too short or empty")
                return False

            # Validate confidence score
            if not (0 <= result.confidence_score <= 1):
                logger.error(
                    f"Invalid confidence score: {result.confidence_score}"
                )
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating grading result: {str(e)}")
            return False

    async def evaluate_grading_confidence(
        self,
        result: GradingResult,
        threshold: float = 0.8
    ) -> bool:
        """
        Evaluates whether we can be confident in the grading result.
        
        Args:
            result: The grading result to evaluate
            threshold: Minimum confidence threshold
            
        Returns:
            True if the result meets confidence requirements
        """
        if result.confidence_score < threshold:
            logger.warning(
                f"Low confidence score: {result.confidence_score}"
            )
            return False
            
        return True