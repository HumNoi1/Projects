# backend/app/services/llm_service.py
from llama_cpp import Llama
from typing import Dict, Any
import os
import logging
from pathlib import Path
import torch
import ctypes

from app.services.llm_config import LLMConfig  # สำหรับเรียกใช้ Windows API

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.llm_config = LLMConfig.get_instance()
        self.model = self.llm_config.get_model()
        
    async def generate_response(
        self, 
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> str:
        """สร้างคำตอบจาก prompt"""
        try:
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "User:", "Assistant:"]  # stop tokens
            )
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
            
    async def grade_answer(
        self,
        reference_answer: str,
        student_answer: str,
        criteria: List[Dict[str, Any]],
        language: str = "th"
    ) -> Dict[str, Any]:
        """ตรวจและให้คะแนนคำตอบ"""
        try:
            prompt = self._create_grading_prompt(
                reference_answer,
                student_answer,
                criteria,
                language
            )
            response = await self.generate_response(prompt)
            return self._parse_grading_response(response)
            
        except Exception as e:
            logger.error(f"Error grading answer: {e}")
            raise