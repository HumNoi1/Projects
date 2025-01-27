from datetime import datetime
from typing import Dict, Any, List
import json
import logging
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

class LMStudioService:
    def __init__(self):
        self.api_base = settings.LMSTUDIO_API_BASE
        self.headers = {
            "Content-Type": "application/json"
        }
        
    async def generate_completion(self, prompt: str) -> str:
        """
        ส่ง request ไปยัง LM Studio API เพื่อ0ัดการ response
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api.base}/chat/completion",
                    headers=self.headers,
                    json={
                        "message": [
                            {"role": "system", "content": "Ypu are a helpful assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "max_tokens": 4096,
                        "stream": False
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                
                # จัดการ response จาก LM Studio
                result = response.json()
                if "error" in result:
                    raise ValueError(f"LM Studio error: {result['error']}")
                
                # ตรวจสอบโครงสร้าง response ที่ถูกต้อง
                if "choices" not in result:
                    return result.get("response", "")
                
                return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
                
            if "choices" in str(e):
                return '{"error": "Invalid response from LM Studio"}'
            raise
        
    def create_grading_prompt(
        self,
        reference_answer: str,
        student_answer: str,
        criteria: List[Dict[str, Any]],
        language: str = "th"
    ) -> str:
        """ สร้าง prompt สำหรับการตรวจคำตอบ"""
        criteria_text = "\n".join([
            f"{c['name']} (คะแนนเต็ม: {c['max_score']}, น้ำหนัก: {c.get('weight', 1.0)}):\n {c.get('description', '')}"
            for c in criteria
        ])
        
        return f"""คุณเป็นผู้เชี่ยวชาญในการตรวจข้อสอบ กรุณาตรวจและให้คะแนนตามเกณฑ์ต่อไปนี้:
    
    เกณฑ์การให้คะแนน:
    {criteria_text}
    
    คำตอบอ้างอิง:
    {reference_answer}
    
    คำตอบของนักเรียน:
    {student_answer}
    
    กรุณาตอบในรูปแบบ JSON ดังนี้:
    {{
    "total_score": คะแนนรวม,
    "criteria_scores": {{
        "ชื่อเกณฑ์": คะแนน,
        ...
    }},
    "feedback": "คำแนะนำและข้อเสนอแนะ"
    }}"""

    async def grade_answer(
        self,
        reference_answer: str,
        student_answer: str,
        criteria: Dict[str, Any],
        language: str = "th"
    ) -> Dict[str, Any]:
        """
        ตรวจและให้คะแนนคำตอบโดยใช้ LM Studio
        """
        prompt = self.create_grading_prompt(
            reference_answer,
            student_answer,
            criteria,
            language
        )
        
        try:
            response = await self.generate_completion(prompt)
            result = json.loads(response)
            
            # Add metadata
            result.update({
                "grading_time": datetime.now().isoformat(),
                "evaluator_id": "lm-studio-grader"
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error grading answer: {str(e)}")
            raise