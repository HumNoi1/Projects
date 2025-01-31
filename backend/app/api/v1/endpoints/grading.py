# app/api/v1/endpoints/grading.py
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.grading_service import GradingService
from app.models.grading import GradingRequest, GradingResponse

router = APIRouter()
grading_service = GradingService()

@router.post("/grade/", response_model=GradingResponse)
async def grade_assignment(request: GradingRequest) -> Dict[str, Any]:
    """
    API endpoint สำหรับการตรวจงาน
    """
    try:
        result = await grading_service.grade_assignment(
            student_answer=request.student_answer,
            reference_answer=request.reference_answer,
            rubric=request.rubric
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error grading assignment: {str(e)}"
        )