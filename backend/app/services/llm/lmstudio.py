# app/services/llm/lmstudio.py
import httpx
from typing import List, Dict, Any, Optional
from app.core.config import settings
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class LMStudioClient:
    """Client for interacting with LM-Studio API."""
    
    def __init__(self):
        self.api_base = settings.LMSTUDIO_API_BASE
        self.embedding_model = settings.EMBEDDING_MODEL_NAME
        self.llm_model = settings.LLM_MODEL_NAME
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        self.timeout = settings.REQUEST_TIMEOUT
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for a list of texts using LM-Studio.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
            
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_base}/v1/embeddings",
                    json={
                        "model": self.embedding_model,
                        "input": texts
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # Extract embeddings from response
                embeddings = [item["embedding"] for item in data["data"]]
                return embeddings
                
        except Exception as e:
            logger.error(f"Error creating embeddings with LM-Studio: {str(e)}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate text completion using LM-Studio.
        
        Args:
            prompt: The prompt to complete
            system_prompt: Optional system prompt for context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_base}/v1/chat/completions",
                    json={
                        "model": self.llm_model,
                        "messages": messages,
                        "max_tokens": max_tokens or self.max_tokens,
                        "temperature": temperature or self.temperature
                    }
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
        except httpx.TimeoutException:
            error_msg = "Request to LM-Studio timed out. Please check if the service is running."
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error generating completion: {str(e)}"
            logger.error(error_msg)
            raise