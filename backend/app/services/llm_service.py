from llama_cpp import Llama
from typing import Dict, Any
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # กำหนดพาธไปยังโมเดล
        model_path = Path("models\llama3.2-typhoon2-3b-instruct-q4_k_m.gguf")
        
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {model_path}. Please download the model first."
            )
            
        # สร้าง Llama instance พร้อมการตั้งค่าที่เหมาะสม
        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=4096,  # ขนาด context window
            n_batch=512,  # batch size สำหรับ inference
            n_threads=4,  # จำนวน CPU threads
            n_gpu_layers=32  # จำนวน layers ที่จะใช้ GPU (ถ้ามี)
        )

    async def generate_response(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 1024,
        stop: list = None
    ) -> Dict[str, Any]:
        """
        สร้างคำตอบจาก prompt ที่กำหนด
        """
        try:
            # สร้าง system prompt ที่เหมาะสมกับ LLaMA
            system_prompt = (
                "You are an expert academic grader. "
                "You must analyze and grade student answers based on reference answers and criteria. "
                "Always provide detailed feedback and numerical scores. "
                "Output must be in JSON format."
            )
            
            # รวม prompt ในรูปแบบที่ LLaMA ต้องการ
            full_prompt = f"""<s>[INST] {system_prompt}

{prompt} [/INST]"""

            # เรียกใช้ model
            response = self.llm(
                full_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop or ["</s>", "[INST]"],
                echo=False
            )

            return {
                "content": response["choices"][0]["text"],
                "usage": {
                    "prompt_tokens": response["usage"]["prompt_tokens"],
                    "completion_tokens": response["usage"]["completion_tokens"],
                    "total_tokens": response["usage"]["total_tokens"]
                }
            }

        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            raise