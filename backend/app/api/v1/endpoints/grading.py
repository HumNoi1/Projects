from fastapi import APIRouter, HTTPException, Depends
from app.models.grading import GradingRequest, GradingResult
from app.services.grading_service import GradingService
from app.services.document_processor import DocumentProcessor
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/grade/", response_model=GradingResult)
async def grade_assignment(request: GradingRequest):
    """
    Grade a student's answer based on reference answer and criteria
    """
    try:
        grading_service = GradingService()
        doc_processor = DocumentProcessor()
        
        # Fetch answers from database (to be implemented)
        # For now using dummy data
        reference_answer = "Sample reference answer"
        student_answer = "Sample student answer"
        
        # Process grading
        result = await grading_service.grade_answer(
            reference_answer=reference_answer,
            student_answer=student_answer,
            criteria=request.criteria,
            language=request.language
        )
        
        # Validate result
        is_valid = await grading_service.validate_grading_result(
            result=result,
            criteria=request.criteria
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail="Invalid grading result generated"
            )
        
        # Store result in database (to be implemented)
        
        return result

    except Exception as e:
        logger.error(f"Error in grading endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))