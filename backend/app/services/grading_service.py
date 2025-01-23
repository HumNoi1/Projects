from datetime import datetime
import json
import logging
from typing import List, Dict, Any
from urllib import response
from app.models.grading import GradingCriteria, GradingResult
from app.services.llm_service import LLMService

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
        self.llm_service = LLMService()

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
        """ตรวจให้คะแนนคำตอบและจัดการผลลัพธ์อย่างระมัดระวัง"""
        try:
            prompt = await self.create_grading_prompt(
                criteria=criteria,
                reference_answer=reference_answer,
                student_answer=student_answer,
                language=language
            )
            
            # เรียกใช้ LLM ในการประมวลผลคำตอบ
            response = await self.llm_service.generate_response(prompt)
            
            try:
                content = response['content'].strip()
                logger.debug(f"Raw LLM response: {content}")
                
                # หาและแยก JSON ชุดแรกที่สมบูรณ์
                json_start = content.find('{')
                if json_start == -1:
                    raise ValueError("No JSON object found in response")
                
                # นับวงเล็บปีกกาเพื่อหาจุดสิ้นสุด JSON ที่สมบูรณ์
                brace_count = 0
                json_end = -1
                
                for i in range(json_start, len (content)):
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i
                            break
                
                if json_end == -1:
                    raise ValueError("Could no found complete JSON object")
                
                # แยกเฉพาะ JSON ชุดแรก
                json_text = content[json_start:json_end + 1]
                logger.debug(f"Extracted JSON: {json_text}")
                
                try:
                    grading_data = json.loads(json_text)
                    
                    # ตรวจสอบโครงสร้างและประเ๓ทข้อมูล
                    self._validate_grading_data(grading_data)
                    
                    # สร้างและตรวจสอบผลลัพธ์
                    result = GradingResult(
                        **grading_data,
                        grading_time=datetime.now(),
                        evaluator_id="Llama-3.2-3B-Instruct-Q4_K_M.gguf"
                    )
                    
                    if not await self.validate_grading_result(result, criteria):
                        raise ValueError("Invalid grading result")
                    
                    return result
                
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing JSON: {str(e)}")
                    logger.error(f"Attempted to parse: {json_text}")
                    raise ValueError(f"Invalid JSON format: {str(e)}")
            
            except Exception as e:
                logger.error(f"Error processing LLM response: {str(e)}")
                raise
        
        except Exception as e:
            logger.error(f"Error in grading process: {str(e)}")
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