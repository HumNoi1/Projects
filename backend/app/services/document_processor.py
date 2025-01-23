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

    async def process_document(self, content: str) -> List[Document]:
        """แยกเอกสารเป็น chunks"""
        # ทำความสะอาดข้อความก่อน
        cleaned_content = self._clean_text(content)
        
        # แยกเอกสารเป็น chunks
        chunks = self.text_splitter.create_documents([cleaned_content])
        return chunks

    async def process_and_embed_documents(
        self,
        content: str,
        metadata: Dict[Any, Any]
    ) -> Dict[str, Any]:
        """Process และสร้าง embeddings สำหรับเอกสาร"""
        try:
            # แยกเอกสารเป็น chunks
            chunks = await self.process_document(content)
            
            # สร้าง embeddings
            texts = [chunk.page_content for chunk in chunks]
            embeddings = await self.embedding_service.create_embeddings(texts)
            
            # เตรียม metadata สำหรับแต่ละ chunk
            chunk_metadata = [
                {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                for i in range(len(chunks))
            ]
            
            # เก็บ embeddings พร้อม metadata
            embedding_ids = await self.embedding_service.store_embeddings(
                embeddings, chunk_metadata
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
        """ทำความสะอาดและ normalize เนื้อหาข้อความ"""
        # ลบช่องว่างที่ไม่จำเป็น
        text = " ".join(text.split())
        return text