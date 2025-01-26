from typing import List, Dict, Any
import json
import logging
from datetime import datetime
from pathlib import Path
from httpx import stream
from app.core.config import settings
from ctranformers import AutoModelForCausalLM

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # ใช้ GPU ถ้ามี
        self.model = AutoModelForCausalLM.from_pretrained(
            settings.LLM_MODEL_PATH,
            model_type="llama",
            gpu_layers=settings.LLM_N_GPU_LAYERS,  # จำนวน layers ที่จะใช้ GPU
            context_length=settings.LLM_N_CTX
        )

    def _create_grading_prompt(
        self,
        reference_answer: str,
        student_answer: str,
        criteria: List[Dict[str, Any]],
        language: str
    ) -> str:
        """Create a prompt for grading based on the given parameters"""
        # Format criteria into a readable string
        criteria_text = "\n".join([
            f"- {c['name']} (max score: {c['max_score']}, weight: {c.get('weight', 1.0)})"
            for c in criteria
        ])

        # Create the prompt template
        system_prompt = {
            "th": """คุณเป็นผู้ตรวจข้อสอบที่มีความเชี่ยวชาญ โปรดตรวจคำตอบของนักเรียนตามเกณฑ์ที่กำหนด
            และให้คะแนนพร้อมคำแนะนำที่เป็นประโยชน์""",
            "en": """You are an expert grader. Please evaluate the student's answer based on the given criteria
            and provide scores with helpful feedback."""
        }.get(language, "th")

        prompt = f"""{system_prompt}

เกณฑ์การให้คะแนน:
{criteria_text}

คำตอบอ้างอิง:
{reference_answer}

คำตอบของนักเรียน:
{student_answer}

โปรดให้คะแนนในรูปแบบ JSON ดังนี้:
{{
    "total_score": คะแนนรวม,
    "criteria_scores": {{
        "ชื่อเกณฑ์": คะแนน,
        ...
    }},
    "feedback": "คำแนะนำและข้อเสนอแนะ"
}}"""

        return prompt

    async def generate(self, prompt: str) -> str:
        try:
            response = self.model(
                prompt,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.9,
                stream=False
            )
            return response
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    async def grade_answer(
        self,
        reference_answer: str,
        student_answer: str,
        criteria: List[Dict[str, Any]],
        language: str = "th"
    ) -> Dict[str, Any]:
        """ตรวจและให้คะแนนคำตอบ"""
        try:
            # Create grading prompt
            prompt = self._create_grading_prompt(
                reference_answer,
                student_answer,
                criteria,
                language
            )

            # Generate response from LLM
            response = await self.generate_response(prompt)

            # Parse response as JSON
            result = json.loads(response)

            # Add additional metadata
            result.update({
                "confidence_score": 0.95,  # Example confidence score
                "grading_time": datetime.now().isoformat(),
                "evaluator_id": "llama-3.2-typhoon2"
            })

            return result

        except Exception as e:
            logger.error(f"Error grading answer: {str(e)}")
            raise

    async def validate_grading_result(
        self,
        result: Dict[str, Any],
        criteria: List[Dict[str, Any]]
    ) -> bool:
        """ตรวจสอบความถูกต้องของผลการให้คะแนน"""
        try:
            # Check required fields
            required_fields = ["total_score", "criteria_scores", "feedback"]
            if not all(field in result for field in required_fields):
                return False

            # Validate criteria scores
            for criterion in criteria:
                name = criterion["name"]
                max_score = criterion["max_score"]
                
                if name not in result["criteria_scores"]:
                    return False
                    
                score = result["criteria_scores"][name]
                if not (0 <= score <= max_score):
                    return False

            # Validate total score
            max_total = sum(c["max_score"] * c.get("weight", 1.0) for c in criteria)
            if not (0 <= result["total_score"] <= max_total):
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating grading result: {str(e)}")
            return False