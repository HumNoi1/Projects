from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import Optional
from app.infrastructure.database.database import get_db
from app.domain.services.file_service import FileService
from app.utils.pdf_processor import extract_text_from_pdf
import os
from app.core.config import settings

router = APIRouter()

@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    file_type: str = Form(...),
    assignment_id: str = Form(...),
    db = Depends(get_db)
):
    """
    Upload a file (teacher answer key or student submission).
    """
    try:
        # Validate file type
        if file_type not in ["teacher", "student"]:
            raise HTTPException(status_code=400, detail="Invalid file type. Must be 'teacher' or 'student'")
        
        # Validate file format (only PDF allowed)
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Create upload directory if it doesn't exist
        upload_path = os.path.join(settings.UPLOAD_DIR, assignment_id)
        os.makedirs(upload_path, exist_ok=True)
        
        # Save file locally
        file_service = FileService(db)
        file_path = await file_service.save_file(file, file_type, assignment_id)
        
        # Extract text from PDF
        text_content = extract_text_from_pdf(file_path)
        
        # Store file info in database
        file_record = await file_service.create_file_record(
            file_name=file.filename,
            file_path=file_path,
            file_type=file_type,
            file_size=os.path.getsize(file_path),
            mime_type=file.content_type,
            assignment_id=assignment_id,
            text_content=text_content
        )
        
        return file_record
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}\n{traceback_str}")