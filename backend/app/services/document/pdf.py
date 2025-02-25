# app/services/document/pdf.py
from typing import List, Dict, Any
import fitz  # PyMuPDF
import logging
from pathlib import Path
from llama_index import Document

logger = logging.getLogger(__name__)

class PDFService:
    """Service for processing PDF documents."""
    
    def __init__(self):
        self.supported_types = {'.pdf'}

    async def extract_text(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract text from PDF, separating by pages."""
        try:
            # Check file type
            if file_path.suffix.lower() not in self.supported_types:
                raise ValueError(f"Unsupported file type: {file_path.suffix}")

            pages = []
            doc = fitz.open(file_path)

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                # Create metadata for the page
                page_data = {
                    'content': text,
                    'metadata': {
                        'page_number': page_num + 1,
                        'total_pages': len(doc),
                        'file_name': file_path.name,
                        'file_path': str(file_path)
                    }
                }
                pages.append(page_data)

            return pages
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise

    async def pdf_to_llama_documents(
        self, 
        file_path: Path,
        additional_metadata: Dict[str, Any] = None
    ) -> List[Document]:
        """Convert PDF to LlamaIndex Document objects."""
        try:
            pages = await self.extract_text(file_path)
            
            documents = []
            for page in pages:
                # Combine default and additional metadata
                metadata = page['metadata'].copy()
                if additional_metadata:
                    metadata.update(additional_metadata)
                
                # Create LlamaIndex Document
                document = Document(
                    text=page['content'],
                    metadata=metadata
                )
                documents.append(document)
            
            return documents
        except Exception as e:
            logger.error(f"Error converting PDF to LlamaIndex documents: {str(e)}")
            raise