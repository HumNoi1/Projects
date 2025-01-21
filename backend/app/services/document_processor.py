from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from app.db.session import get_milvus
from .embedding_service import EmbeddingService
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, db_manager=None):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        self.embedding_service = EmbeddingService()
        self.db_manager = db_manager
    
    async def get_db(self):
        """Get database connection"""
        if self.db_manager:
            return self.db_manager
        return await get_milvus()

    async def process_and_embed_documents(
        self,
        content: str,
        metadata: Dict[Any, Any]  
    ) -> Dict[str, Any]:
        """Process and create embed documents"""
        try:
            #process document into chunks
            chunks = await self.process_and_embed_documents(content, metadata)
            
            #create embeddings
            texts = [chunk.page_content for chunk in chunks]
            embedding = await self.embedding_service.create_embeddings(texts)
            
            #store embeddings with metadata
            chunk_metadata = [
                {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                for i in range(len(chunks))
            ]
            
            embedding_ids = await self.embedding_service.store_embeddings(
                embedding, chunk_metadata
            )
            
            return {
                "success": True,
                "embedding_ids": embedding_ids,
                "chunk_count": len(chunks)
            }
        
        except Exception as e:
            logger.error(f"Error in document processing pipeline: {str(e)}")
            raise

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Remove special characters but keep Thai characters
        # Add more specific cleaning rules as needed
        
        return text