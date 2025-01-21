from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from typing import List, Dict, Any
from app.models.grading import GradingCriteria, GradingResult
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class GradingService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.0
        )
        
    async def create_grading_prompt(
        self,
        criteria: List[GradingCriteria],
        reference_answer: str,
        student_answer: str,
        language: str
    ) -> str:
        """Create a structured prompt for grading"""
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert grader for academic assignments.
            Grade the student's answer based on the reference answer and given criteria.
            Provide detailed feedback and scores.
            
            Output format must be valid JSON with the following structure:
            {
                "criteria_scores": {"criteria_name": score},
                "total_score": float,
                "feedback": "detailed feedback",
                "confidence_score": float between 0-1
            }"""),
            ("user", """Reference Answer: {reference}
            
            Student Answer: {student_answer}
            
            Grading Criteria:
            {criteria_json}
            
            Language: {language}
            
            Please grade the answer and provide structured feedback.""")
        ])
        
        return prompt_template

    async def grade_answer(
        self,
        reference_answer: str,
        student_answer: str,
        criteria: List[GradingCriteria],
        language: str = "th"
    ) -> GradingResult:
        """Grade student answer using LLM"""
        try:
            # Create grading chain
            prompt = await self.create_grading_prompt(
                criteria=criteria,
                reference_answer=reference_answer,
                student_answer=student_answer,
                language=language
            )
            
            grading_chain = LLMChain(
                llm=self.llm,
                prompt=prompt
            )
            
            # Execute grading with token tracking
            with get_openai_callback() as cb:
                result = await grading_chain.arun({
                    "reference": reference_answer,
                    "student_answer": student_answer,
                    "criteria_json": [c.dict() for c in criteria],
                    "language": language
                })
            
            # Parse LLM response
            grading_data = json.loads(result)
            
            return GradingResult(
                **grading_data,
                grading_time=datetime.now(),
                evaluator_id="gpt-4"
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