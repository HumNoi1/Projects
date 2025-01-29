# app/services/pdf_service.py
from typing import List, Dict, Any
import fitz  # PyMuPDF
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFService:
    """
    บริการจัดการไฟล์ PDF รวมถึงการแปลงเป็นข้อความและแยกส่วน
    คลาสนี้รับผิดชอบการอ่านไฟล์ PDF และเตรียมข้อมูลสำหรับการสร้าง embeddings
    """
    def __init__(self):
        self.supported_types = {'.pdf'}

    async def extract_text(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        แปลง PDF เป็นข้อความโดยแยกเป็นหน้าๆ
        
        Args:
            file_path: Path ของไฟล์ PDF
            
        Returns:
            List ของ Dict ที่มีข้อมูลแต่ละหน้า โดยมี metadata กำกับ
        """
        try:
            # ตรวจสอบนามสกุลไฟล์
            if file_path.suffix.lower() not in self.supported_types:
                raise ValueError(f"Unsupported file type: {file_path.suffix}")

            pages = []
            doc = fitz.open(file_path)

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                # สร้าง metadata สำหรับแต่ละหน้า
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