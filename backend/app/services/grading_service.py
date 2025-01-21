from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from typing import List, Dict, Any
from app.models.grading import GradingCriteria, GradingResult
from datetime import datetime
import json
import logging

from backend.app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class GradingService:
    def __init__(self):
        self.llm_service = LLMService()
        
    async def create_grading_prompt(
        self,
        criteria: List[GradingCriteria],
        reference_answer: str,
        student_answer: str,
        language: str
    ) -> str:
        """Create a structured prompt for grading"""
        
        # Create grading prompt for llama
        criteria_text = "\n".join([
            f"- {c.name} (max score: {c.max_score}, weight: {c.weight}):\n {c.description}"
            for c in criteria
        ])
        
        prompt = f"""Please grade the following student answer based on the reference answer and criteria.
        
        Reference answer:
        {reference_answer}
        
        Student answer:
        {student_answer}
        
        Grading criteria:
        {criteria_text}
        
        Language for feedback: {language}
        
        please provide your evaluation and score in the following JSON format:
        {{
            "criteria_scores"; {{"criteria_name": score}},
            "total_score": float,
            "feedback": "detailed feedback in {language}"
            "confidence_score": float between 0-1
        }}"""
        
        return prompt

    async def grade_answer(
        self,
        reference_answer: str,
        student_answer: str,
        criteria: List[GradingCriteria],
        language: str = "th"
    ) -> GradingResult:
        """
        ตรวจให้คะแนนคำตอบของนักเรียนโดยใช้ LLaMA
        """
        try:
            # create grading prompt
            prompt = await self.create_grading_prompt(
                criteria=criteria,
                reference_answer=reference_answer,
                student_answer=student_answer,
                language=language
            )
            
            # เรียกใช้ Llama
            response = await self.llm_service.generate_response(
                prompt=prompt,
                temperature=0.1, 
            )
            
            # แปลงคำตอบจาก LLaMA ให้เป็น JSON
            try:
                grading_result = json.loads(response["content"])
            except json.JSONDecodeError:
                # ถ้าแปลง JSON ให้ลองทำความสะอาดข้อมูลก่อน
                cleaned_content = response["content"].strip()
                # หา JSON block แรกที่เจอ
                start = cleaned_content.find("{")
                end = cleaned_content.rfind("}")
                grading_data = cleaned_content[start:end]
            return GradingResult(
                **grading_data,
                grading_time=datetime.nom(),
                evaluator_id="llama-3.2-typhoon22-3b"
            )
        
        except Exception as e:
            logger.error(f"Error in grading process: {str(e)}")
            raise

    async def validate_grading_result(
        self,
        result: GradingResult,
        criteria: List[GradingCriteria]
    ) -> bool:
        """Validate grading results against criteria"""
        try:
            # Check if all criteria are graded
            graded_criteria = set(result.criteria_scores.keys())
            expected_criteria = set(c.name for c in criteria)
            if graded_criteria != expected_criteria:
                return False
            
            # Validate score ranges
            total_max_score = sum(c.max_score * c.weight for c in criteria)
            if result.total_score < 0 or result.total_score > total_max_score:
                return False
                
            # Validate individual criteria scores
            for criterion in criteria:
                score = result.criteria_scores.get(criterion.name, 0)
                if score < 0 or score > criterion.max_score:
                    return False
            
            return True

        except Exception as e:
            logger.error(f"Error validating grading result: {str(e)}")
            return False