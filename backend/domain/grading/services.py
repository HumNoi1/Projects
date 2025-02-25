# domain/grading/services.py
from typing import Dict, Any, List
import json
import logging
from llama_index import Document
from app.services.llm.index import LlamaIndexService
from app.services.llm.lmstudio import LMStudioClient

logger = logging.getLogger(__name__)

class GradingServiceError(Exception):
    """Custom exception for GradingService."""
    pass

class GradingService:
    """Service for grading assignments using LLM."""
    
    def __init__(self):
        self.llama_index_service = LlamaIndexService()
        self.lmstudio_client = LMStudioClient()
    
    def validate_rubric(self, rubric: Dict[str, Any]) -> None:
        """Validate rubric format."""
        if not isinstance(rubric, dict):
            raise GradingServiceError("Rubric must be a dictionary")
            
        required_fields = {'weight', 'criteria'}
        for criterion, details in rubric.items():
            if not isinstance(details, dict):
                raise GradingServiceError(
                    f"Each criterion must be a dictionary, got {type(details)} for {criterion}"
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
        """Grade an assignment by comparing student answer to reference answer."""
        # Validate inputs
        if not student_answer or not reference_answer or not rubric:
            raise GradingServiceError("Missing required input: student_answer, reference_answer, and rubric are required")
            
        # Validate rubric format
        self.validate_rubric(rubric)

        try:
            # Create system prompt with context and instructions
            system_prompt = """You are an expert grader who evaluates student assignments with fairness and precision.
            Your task is to grade a student answer based on a reference answer and a provided rubric.
            Analyze both texts carefully and provide:
            1. A numerical score out of 100
            2. Detailed feedback explaining strengths and weaknesses
            3. A breakdown of points for each rubric criterion
            4. Suggestions for improvement"""
            
            # Create prompt for grading
            grading_prompt = f"""
            # Reference Answer
            {reference_answer}
            
            # Student Answer
            {student_answer}
            
            # Rubric
            {json.dumps(rubric, indent=2)}
            
            Please analyze the student's answer against the reference answer using the rubric criteria.
            Provide your evaluation in the following JSON format:
            
            ```json
            {{
                "score": 85,
                "feedback": "Your detailed feedback here...",
                "criterion_scores": {{
                    "criterion1": 90,
                    "criterion2": 80,
                    ...
                }},
                "strengths": ["strength1", "strength2", ...],
                "areas_for_improvement": ["area1", "area2", ...]
            }}
            ```
            
            Ensure all scores are numerical values. The overall score should reflect the weighted average based on the rubric weights.
            """
            
            # Use LMStudio for grading
            grading_result = await self.lmstudio_client.generate_completion(
                prompt=grading_prompt,
                system_prompt=system_prompt,
                temperature=0.3  # Lower temperature for more deterministic results
            )
            
            # Parse the JSON response
            try:
                # Extract JSON from response (which might contain markdown code blocks)
                json_str = grading_result
                if "```json" in grading_result:
                    json_str = grading_result.split("```json")[1].split("```")[0].strip()
                elif "```" in grading_result:
                    json_str = grading_result.split("```")[1].split("```")[0].strip()
                
                parsed_result = json.loads(json_str)
                
                return {
                    "success": True,
                    "grading_result": parsed_result
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw result
                logger.warning("Failed to parse JSON from LLM response")
                return {
                    "success": True,
                    "grading_result": {
                        "raw_response": grading_result
                    }
                }
                
        except Exception as e:
            logger.error(f"Error grading assignment: {str(e)}")
            raise GradingServiceError(f"Failed to grade assignment: {str(e)}")