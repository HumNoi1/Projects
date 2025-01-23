from llama_cpp import Llama
from typing import Dict, Any
import os
import logging
from pathlib import Path
from app.core.config import settings  # Adjust the import path according to your project structure

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # กำหนดพาธไปยังโมเดล
        model_path = Path("app/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf")
        
        # ตรวจสอบและสร้างโฟลเดอร์ถ้ายังไม่มี
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not model_path.exists():
            # แจ้งว่าต้องดาวน์โหลด model และวิธีการดาวน์โหลด
            raise FileNotFoundError(
                f"""Model file not found at {model_path}. 
                Please download the model by following these steps:
                1. Download from: https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
                2. Save to: {model_path}
                """
            )

        # สร้าง Llama instance พร้อมการตั้งค่าจาก settings
        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=settings.LLM_N_CTX,
            n_batch=settings.LLM_N_BATCH,
            n_threads=settings.LLM_N_THREADS,
            n_gpu_layers=settings.LLM_N_GPU_LAYERS
        )
        logger.info(f"Successfully loaded LLM model from {model_path}")

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