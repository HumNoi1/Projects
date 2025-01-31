# app/services/document_processor.py
from typing import List, Dict, Any
from pathlib import Path
from .pdf_service import PDFService
from .embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    ประมวลผลเอกสารและสร้าง embeddings
    คลาสนี้ทำหน้าที่เป็นตัวกลางระหว่าง PDF Service และ Embedding Service
    """
    def __init__(self):
        self.pdf_service = PDFService()
        self.embedding_service = EmbeddingService()

    async def process_pdf(
        self,
        file_path: Path,
        additional_metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        ประมวลผลไฟล์ PDF และสร้าง embeddings
        
        Args:
            file_path: Path ของไฟล์ PDF
            additional_metadata: metadata เพิ่มเติมที่ต้องการเก็บ
            
        Returns:
            Dict ที่มีข้อมูลผลการประมวลผล รวมถึง embedding IDs
        """
        try:
            # สกัดข้อความจาก PDF
            pages = await self.pdf_service.extract_text(file_path)
            
            # รวม metadata เพิ่มเติม
            if additional_metadata:
                for page in pages:
                    page['metadata'].update(additional_metadata)

            # สร้าง embeddings สำหรับแต่ละหน้า
            texts = [page['content'] for page in pages]
            metadata_list = [page['metadata'] for page in pages]
            
            embeddings = await self.embedding_service.create_embeddings(texts)
            
            # บันทึก embeddings ลงใน Milvus
            embedding_ids = await self.embedding_service.store_embeddings(
                embeddings,
                metadata_list,
                texts
            )

            return {
                'success': True,
                'total_pages': len(pages),
                'embedding_ids': embedding_ids,
                'file_path': str(file_path)
            }

        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise