# app/api/v1/endpoints/grading.py
from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from pathlib import Path
import tempfile
import shutil
import json
import logging
from typing import Dict, Any
from domain.grading.services import GradingService, GradingServiceError
from app.services.document.pdf import PDFService

router = APIRouter()
logger = logging.getLogger(__name__)
grading_service = GradingService()
pdf_service = PDFService()

@router.post("/grade-text/", response_model=Dict[str, Any])
async def grade_from_text(
    student_answer: str = Form(...),
    reference_answer: str = Form(...),
    rubric: str = Form(...)  # JSON string
):
    """Grade assignment from text inputs."""
    try:
        # Parse rubric from JSON string
        try:
            rubric_dict = json.loads(rubric)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid rubric JSON format"
            )
        
        # Grade the assignment
        result = await grading_service.grade_assignment(
            student_answer=student_answer,
            reference_answer=reference_answer,
            rubric=rubric_dict
        )
        
        return result
        
    except GradingServiceError as e:
        logger.error(f"Grading service error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error grading assignment: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error grading assignment: {str(e)}"
        )

@router.post("/grade-pdf/", response_model=Dict[str, Any])
async def grade_from_pdf(
    teacher_file: UploadFile = File(...),
    student_file: UploadFile = File(...),
    rubric: str = Form(...)  # JSON string
):
    """Grade assignment from PDF files."""
    # Check file types
    if not teacher_file.filename.lower().endswith('.pdf') or not student_file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Create temporary files
    teacher_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    student_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    
    try:
        # Save uploaded files
        teacher_content = await teacher_file.read()
        student_content = await student_file.read()
        
        teacher_temp.write(teacher_content)
        student_temp.write(student_content)
        teacher_temp.close()
        student_temp.close()
        
        # Extract text from PDFs
        teacher_pages = await pdf_service.extract_text(Path(teacher_temp.name))
        student_pages = await pdf_service.extract_text(Path(student_temp.name))
        
        # Combine text from all pages
        teacher_text = "\n".join(page["content"] for page in teacher_pages)
        student_text = "\n".join(page["content"] for page in student_pages)
        
        # Parse rubric from JSON string
        try:
            rubric_dict = json.loads(rubric)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid rubric JSON format"
            )
        
        # Grade the assignment
        result = await grading_service.grade_assignment(
            student_answer=student_text,
            reference_answer=teacher_text,
            rubric=rubric_dict
        )
        
        return result
        
    except GradingServiceError as e:
        logger.error(f"Grading service error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error grading from PDF: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error grading from PDF: {str(e)}"
        )
    finally:
        # Clean up temporary files
        Path(teacher_temp.name).unlink(missing_ok=True)
        Path(student_temp.name).unlink(missing_ok=True)