# app/api/v1/endpoints/documents.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import tempfile
import shutil
import logging
from typing import List, Dict, Any
from app.services.document_processor import DocumentProcessor

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload/pdf/", response_model=Dict[str, Any])
async def upload_pdf(
    file: UploadFile = File(...),
    class_id: int = None,
    assignment_id: int = None
):
    """
    อัพโหลดและประมวลผลไฟล์ PDF
    
    Args:
        file: ไฟล์ PDF ที่อัพโหลด
        class_id: ID ของชั้นเรียน (ถ้ามี)
        assignment_id: ID ของงานที่มอบหมาย (ถ้ามี)
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # สร้าง temporary file สำหรับเก็บไฟล์ที่อัพโหลด
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        try:
            # บันทึกไฟล์ที่อัพโหลด
            shutil.copyfileobj(file.file, temp_file)
            
            # สร้าง metadata เพิ่มเติม
            additional_metadata = {
                'class_id': class_id,
                'assignment_id': assignment_id,
                'original_filename': file.filename
            }
            
            # ประมวลผล PDF
            processor = DocumentProcessor()
            result = await processor.process_pdf(
                Path(temp_file.name),
                additional_metadata
            )
            
            return result

        except Exception as e:
            logger.error(f"Error processing uploaded PDF: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing PDF: {str(e)}"
            )
        finally:
            # ลบไฟล์ชั่วคราว
            Path(temp_file.name).unlink(missing_ok=True)