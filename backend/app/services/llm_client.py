# app/services/llm_client.py
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class LMStudioLLMClient:
    def __init__(self):
        self.api_base = settings.LMSTUDIO_API_BASE
        self.model = settings.LLM_MODEL_NAME
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        self.timeout = settings.REQUEST_TIMEOUT  # เพิ่ม timeout
        
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # ทดสอบการเชื่อมต่อก่อน
                try:
                    await client.get(self.api_base)
                except Exception as e:
                    logger.error(f"LM-Studio API is not accessible: {str(e)}")
                    return "Error: LM-Studio API is not accessible. Please ensure LM-Studio is running."

                response = await client.post(
                    f"{self.api_base}/v1/chat/completions",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                        "temperature": kwargs.get("temperature", self.temperature),
                    }
                )
                response.raise_for_status()
                result_json = await response.json()
                result = result_json["choices"][0]["message"]["content"]
                return result
                
        except httpx.TimeoutException:
            error_msg = "Request to LM-Studio timed out. Please check if LM-Studio is running and responsive."
            logger.error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error generating LLM response: {str(e)}"
            logger.error(error_msg)
            return error_msg