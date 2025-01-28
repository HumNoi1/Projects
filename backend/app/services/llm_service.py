from typing import Dict, Any, Optional, List
import httpx
import json
import logging
from datetime import datetime
from app.core.config import settings
from app.models.grading import GradingCriteria, GradingResult

logger = logging.getLogger(__name__)

class LLMService:
    """
    Service class for interacting with LM Studio's local inference server.
    Provides methods for generating responses and grading answers using the OpenAI-compatible API.
    """
    
    def __init__(self):
        # Initialize service with configuration from settings
        self.api_base = settings.LMSTUDIO_API_BASE
        self.headers = {
            "Content-Type": "application/json"
        }
        self.default_system_prompt = "You are a helpful AI assistant specializing in grading and assessment."
        
    async def _make_request(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """
        Makes HTTP request to LM Studio API with error handling and logging.
        
        Args:
            endpoint: API endpoint (e.g., "chat/completions")
            payload: Request data
            timeout: Request timeout in seconds
            
        Returns:
            API response as dictionary
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.api_base}/{endpoint}",
                    headers=self.headers,
                    json=payload,
                    timeout=timeout
                )
                response.raise_for_status()
                return response.json()
                
            except httpx.RequestError as e:
                logger.error(f"Network error when calling LM Studio: {str(e)}")
                raise Exception(f"Failed to connect to LM Studio: {str(e)}")
                
            except httpx.HTTPStatusError as e:
                logger.error(f"LM Studio API error: {str(e)}")
                raise Exception(f"LM Studio API error: {str(e)}")
                
            except Exception as e:
                logger.error(f"Unexpected error in LM Studio request: {str(e)}")
                raise

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generates a response using the LM Studio API.
        
        Args:
            prompt: The user's input prompt
            system_prompt: Optional system prompt to override default
            temperature: Optional temperature parameter for response randomness
            max_tokens: Optional maximum tokens in response
            
        Returns:
            Generated response text
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": system_prompt or self.default_system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            payload = {
                "messages": messages,
                "temperature": temperature or settings.LLM_TEMPERATURE,
                "max_tokens": max_tokens or settings.LLM_MAX_TOKENS,
                "top_p": settings.LLM_TOP_P,
                "stream": False
            }
            
            response = await self._make_request("chat/completions", payload)
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    async def grade_answer(
        self,
        reference_answer: str,
        student_answer: str,
        criteria: List[GradingCriteria],
        language: str = "th"
    ) -> GradingResult:
        """
        ตรวจและให้คะแนนคำตอบโดยใช้ LM Studio API
        """
        try:
            # สร้าง system prompt ที่ชัดเจนขึ้น
            system_prompt = """You are an expert grader. You must:
            1. Read and understand the reference answer
            2. Evaluate the student answer based on given criteria
            3. Return response in EXACT JSON format
            4. Calculate total_score as weighted average of criteria scores
            5. Provide detailed feedback in Thai language
            6. Ensure all numeric values are plain numbers, not formulas"""

            # Format criteria ให้ชัดเจน
            criteria_text = "\n".join([
                f"- {c.name} (max_score={c.max_score}, weight={c.weight}): {c.description}"
                for c in criteria
            ])

            # สร้าง prompt ที่ระบุรูปแบบ JSON ที่ต้องการอย่างชัดเจน
            grading_prompt = f"""กรุณาตรวจให้คะแนนตามเกณฑ์ต่อไปนี้:

            เกณฑ์การให้คะแนน:
            {criteria_text}

            คำตอบมาตรฐาน:
            {reference_answer}

            คำตอบของนักเรียน:
            {student_answer}

            โปรดส่งผลการตรวจในรูปแบบ JSON ดังนี้ (ห้ามใส่สูตรคำนวณ ให้ใส่ตัวเลขเท่านั้น):
            {{
                "criteria_scores": {{
                    "ความครบถ้วนของเนื้อหา": [คะแนน 0-10],
                    "ความถูกต้องของการอธิบาย": [คะแนน 0-10],
                    "การยกตัวอย่างและการประยุกต์ใช้": [คะแนน 0-10]
                }},
                "total_score": [คะแนนรวมถ่วงน้ำหนักแล้ว 0-10],
                "feedback": "[คำแนะนำเป็นภาษาไทย]",
                "confidence_score": [ความมั่นใจ 0-1]
            }}"""

            # Generate grading response
            response_text = await self.generate_response(
                prompt=grading_prompt,
                system_prompt=system_prompt,
                temperature=0.3  # Lower temperature for more consistent grading
            )
            
            # Parse JSON response
            try:
                # Find and extract the JSON object from the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start == -1 or json_end == 0:
                    raise ValueError("No JSON object found in response")
                
                json_str = response_text[json_start:json_end]
                result_dict = json.loads(json_str)
                
                # Create GradingResult object
                result = GradingResult(
                    **result_dict,
                    grading_time=datetime.now(),
                    evaluator_id="lmstudio-local"
                )
                
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {str(e)}")
                logger.error(f"Raw response: {response_text}")
                raise ValueError(f"Invalid JSON in LLM response: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error in grading process: {str(e)}")
            raise

    async def validate_result_format(self, result: Dict[str, Any], criteria: List[GradingCriteria]) -> bool:
        """
        Validates the format and values of a grading result.
        
        Args:
            result: The grading result to validate
            criteria: The grading criteria used
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check required fields
            required_fields = {'criteria_scores', 'total_score', 'feedback', 'confidence_score'}
            if not all(field in result for field in required_fields):
                return False
            
            # Validate criteria scores
            expected_criteria = {c.name for c in criteria}
            if set(result['criteria_scores'].keys()) != expected_criteria:
                return False
            
            # Validate score ranges
            for criterion in criteria:
                score = result['criteria_scores'].get(criterion.name)
                if not (0 <= score <= criterion.max_score):
                    return False
            
            # Validate total score
            max_total = sum(c.max_score * c.weight for c in criteria)
            if not (0 <= result['total_score'] <= max_total):
                return False
            
            # Validate confidence score
            if not (0 <= result['confidence_score'] <= 1):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating result format: {str(e)}")
            return False