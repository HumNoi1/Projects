# app/services/document/processor.py
from typing import List, Dict, Any
from pathlib import Path
import logging
from llama_index import Document
from app.services.document.pdf import PDFService
from app.services.llm.index import LlamaIndexService

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Service for processing documents and creating vector embeddings."""
    
    def __init__(self):
        self.pdf_service = PDFService()
        self.llama_index_service = LlamaIndexService()

    async def process_pdf(
        self,
        file_path: Path,
        collection_name: str = None,
        additional_metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process PDF document and create vector embeddings."""
        try:
            # Convert PDF to LlamaIndex documents
            documents = await self.pdf_service.pdf_to_llama_documents(
                file_path,
                additional_metadata
            )
            
            # Set collection name (if provided)
            if collection_name:
                self.llama_index_service.vector_store.collection_name = collection_name
            
            # Create index from documents
            index = await self.llama_index_service.create_index_from_documents(documents)
            
            return {
                'success': True,
                'total_pages': len(documents),
                'collection_name': self.llama_index_service.vector_store.collection_name,
                'file_path': str(file_path)
            }
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise