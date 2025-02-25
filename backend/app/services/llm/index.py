# app/services/llm/index.py
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
import asyncio
from llama_index import ServiceContext, VectorStoreIndex, Document
from llama_index.core.node_parser import SentenceSplitter  # แก้ไขจาก llama_index.node_parser
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.llms import CustomLLM  # แก้ไขจาก llama_index.llms.custom
from llama_index.embeddings import BaseEmbedding  # แก้ไขจาก llama_index.embeddings.custom
from app.core.config import settings
from pymilvus import connections
from .lmstudio import LMStudioClient

logger = logging.getLogger(__name__)

class LMStudioEmbedding(BaseEmbedding):
    """Custom embedding class that uses LM-Studio API."""
    
    def __init__(self):
        self.client = LMStudioClient()
        super().__init__()
        
    async def _get_text_embedding(self, text: str) -> List[float]:
        """Get embedding for a single text."""
        embeddings = await self.client.create_embeddings([text])
        if not embeddings:
            raise ValueError("Failed to get embeddings")
        return embeddings[0]
    
    async def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts."""
        return await self.client.create_embeddings(texts)
        
    # เพิ่มเมธอดที่จำเป็นสำหรับ BaseEmbedding
    def get_text_embedding(self, text: str) -> List[float]:
        """Synchronous method for getting embeddings (required)."""
        return asyncio.run(self._get_text_embedding(text))
        
    def get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Synchronous method for getting multiple embeddings (required)."""
        return asyncio.run(self._get_text_embeddings(texts))

class LMStudioLLM(CustomLLM):
    """Custom LLM class that uses LM-Studio API."""
    
    def __init__(self):
        self.client = LMStudioClient()
        super().__init__()
        
    async def acompletion(self, prompt: str, **kwargs) -> str:
        """Complete a prompt."""
        return await self.client.generate_completion(
            prompt=prompt,
            temperature=kwargs.get("temperature", self.client.temperature),
            max_tokens=kwargs.get("max_tokens", self.client.max_tokens)
        )
    
    async def achat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Complete a chat prompt."""
        system_prompt = None
        user_prompt = ""
        
        for message in messages:
            if message["role"] == "system":
                system_prompt = message["content"]
            elif message["role"] == "user":
                user_prompt = message["content"]
        
        return await self.client.generate_completion(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=kwargs.get("temperature", self.client.temperature),
            max_tokens=kwargs.get("max_tokens", self.client.max_tokens)
        )
        
    # เพิ่มเมธอดที่จำเป็นสำหรับ CustomLLM
    def complete(self, prompt: str, **kwargs) -> str:
        """Synchronous completion method (required)."""
        return asyncio.run(self.acompletion(prompt, **kwargs))
        
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Synchronous chat completion method (required)."""
        return asyncio.run(self.achat(messages, **kwargs))