from llama_cpp import Llama
from typing import Dict, Any
import os
import logging
import torch
from pathlib import Path

from regex import T
from app.core.config import settings  # Adjust the import path according to your project structure

logger = logging.getLogger(__name__)

# backend/app/services/llm_service.py
from llama_cpp import Llama
from typing import Dict, Any
import os
import logging
from pathlib import Path
import torch
import ctypes  # สำหรับเรียกใช้ Windows API

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # Windows-specific GPU selection
        try:
            # ตั้งค่าให้ใช้ NVIDIA GPU โดยตรง
            if os.name == 'nt':  # Windows only
                # Load nvml-dll for direct NVIDIA GPU management
                ctypes.CDLL("nvml.dll")
                
                # บังคับให้ใช้ NVIDIA GPU
                os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
                os.environ["CUDA_VISIBLE_DEVICES"] = "1"  # GPU1 = RTX 3050
                
                # เพิ่ม environment variables สำหรับ CUDA
                os.environ["CUDA_PATH"] = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.7"
                os.environ["PATH"] += ";C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.7/bin"
        except Exception as e:
            logger.warning(f"Failed to set NVIDIA GPU preference: {str(e)}")

        # ตรวจสอบ CUDA และ GPU availability
        self.use_gpu = torch.cuda.is_available()
        if self.use_gpu:
            # ดูข้อมูล GPU ทั้งหมดที่มี
            gpu_count = torch.cuda.device_count()
            logger.info(f"Found {gpu_count} CUDA-capable GPU(s)")
            
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                logger.info(f"GPU {i}: {gpu_name} with {gpu_memory:.2f}GB memory")
            
            # เลือกใช้ NVIDIA GPU (GPU1)
            torch.cuda.set_device(1)  # เลือก GPU1 (RTX 3050)
            current_device = torch.cuda.current_device()
            gpu_name = torch.cuda.get_device_name(current_device)
            logger.info(f"Selected GPU {current_device}: {gpu_name}")
            
            # ตั้งค่า GPU memory utilization
            torch.cuda.set_per_process_memory_fraction(0.8, current_device)
        else:
            logger.warning("No CUDA-capable GPU detected. Please check NVIDIA drivers and CUDA installation")
            logger.info("Available GPUs from system:")
            os.system('nvidia-smi')  # แสดงข้อมูล GPU จาก nvidia-smi

        # กำหนดพาธไปยังโมเดล
        model_path = Path("app/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf")
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not model_path.exists():
            raise FileNotFoundError(
                f"""Model file not found at {model_path}. 
                Please download the model by following these steps:
                1. Download from: https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
                2. Save to: {model_path}
                """
            )

        # GPU-specific configurations สำหรับ RTX 3050
        gpu_config = {
            'n_gpu_layers': 35 if self.use_gpu else 0,  # เหมาะสมกับ RTX 3050
            'use_mlock': True,
            'use_mmap': True,
            'verbose': True
        }

        # สร้าง Llama instance
        try:
            self.llm = Llama(
                model_path=str(model_path),
                n_ctx=settings.LLM_N_CTX,
                n_batch=settings.LLM_N_BATCH,
                n_threads=settings.LLM_N_THREADS,
                **gpu_config
            )
            
            # Log GPU utilization หลังโหลดโมเดล
            if self.use_gpu:
                memory_allocated = torch.cuda.memory_allocated(current_device) / (1024**3)
                memory_reserved = torch.cuda.memory_reserved(current_device) / (1024**3)
                logger.info(f"GPU Memory Allocated: {memory_allocated:.2f}GB")
                logger.info(f"GPU Memory Reserved: {memory_reserved:.2f}GB")
            
            logger.info(f"Successfully loaded LLM model from {model_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise

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